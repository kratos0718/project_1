from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.agents.state import ComplaintWorkflowState
from app.models.schemas import AgentReport
from app.config.settings import Settings

class SeverityOutput(BaseModel):
    urgency: str = Field(description="The urgency level: critical, high, medium, or low")
    severity_score: float = Field(description="A float score between 0.0 and 1.0 representing severity risk")
    reasoning: str = Field(description="Brief reasoning for this severity score")

class SummaryOutput(BaseModel):
    summary: str = Field(description="Executive summary grounded in citations")
    reasoning: str = Field(description="Brief reasoning for this summary")

class EscalationOutput(BaseModel):
    escalation_priority: str = Field(description="One of: municipal_emergency_cell, department_supervisor, or ward_officer")
    reasoning: str = Field(description="Brief reasoning for this escalation level")


class ComplaintAgentWorkflow:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        if settings.openai_api_key:
            self.llm = ChatOpenAI(model=settings.llm_model, api_key=settings.openai_api_key, temperature=0)
        else:
            self.llm = None

        graph = StateGraph(ComplaintWorkflowState)
        graph.add_node("planner", self._planner)
        graph.add_node("severity", self._severity)
        graph.add_node("duplicates", self._duplicates)
        graph.add_node("summarizer", self._summarizer)
        graph.add_node("escalation", self._escalation)
        graph.set_entry_point("planner")
        graph.add_edge("planner", "severity")
        graph.add_edge("severity", "duplicates")
        graph.add_edge("duplicates", "summarizer")
        graph.add_edge("summarizer", "escalation")
        graph.add_edge("escalation", END)
        self.graph = graph.compile()

    async def run(self, state: ComplaintWorkflowState) -> AgentReport:
        result = await self.graph.ainvoke({**state, "reasoning_trace": []})
        return AgentReport(
            summary=result["summary"],
            urgency=result["urgency"],
            severity_score=result["severity_score"],
            escalation_priority=result["escalation_priority"],
            duplicate_ids=result["duplicate_ids"],
            citations=result.get("citations", []),
            reasoning_trace=result["reasoning_trace"],
        )

    async def _planner(self, state: ComplaintWorkflowState) -> ComplaintWorkflowState:
        return self._trace(state, "planner", "Route complaint through severity, duplicate, summary, and escalation analysis.")

    async def _severity(self, state: ComplaintWorkflowState) -> ComplaintWorkflowState:
        text = state["text"]
        
        if self.llm:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an AI assistant analyzing civic complaints. Determine the severity score (0.0 to 1.0) and urgency (critical, high, medium, low)."),
                ("human", "Complaint:\n{text}")
            ])
            chain = prompt | self.llm.with_structured_output(SeverityOutput)
            result = await chain.ainvoke({"text": text})
            state["severity_score"] = result.severity_score
            state["urgency"] = result.urgency
            return self._trace(state, "severity", result.reasoning)
        else:
            text_lower = text.lower()
            severe_terms = {"fire", "sewage", "collapse", "accident", "flood", "contamination", "hospital", "school"}
            score = min(1.0, 0.25 + sum(0.12 for term in severe_terms if term in text_lower))
            urgency = "critical" if score >= 0.75 else "high" if score >= 0.55 else "medium" if score >= 0.35 else "low"
            state["severity_score"] = round(score, 2)
            state["urgency"] = urgency
            return self._trace(state, "severity", f"Assigned {urgency} urgency from textual risk indicators.")

    async def _duplicates(self, state: ComplaintWorkflowState) -> ComplaintWorkflowState:
        citations = state.get("citations", [])
        duplicates = [citation.complaint_id for citation in citations if citation.score >= 0.82 and citation.complaint_id != state["complaint_id"]]
        state["duplicate_ids"] = duplicates[:5]
        return self._trace(state, "duplicate_detection", f"Found {len(state['duplicate_ids'])} likely duplicate complaints.")

    async def _summarizer(self, state: ComplaintWorkflowState) -> ComplaintWorkflowState:
        citations = state.get("citations", [])
        
        if self.llm:
            cited = "\n".join(f"- [{c.complaint_id}] {c.excerpt}" for c in citations[:3]) or "No prior citations."
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Write a grounded executive summary for this civic complaint. Incorporate details from the provided citations if they are relevant."),
                ("human", "Category: {category}\nLocality: {locality}\nUrgency: {urgency}\nComplaint: {text}\n\nCitations:\n{cited}")
            ])
            chain = prompt | self.llm.with_structured_output(SummaryOutput)
            result = await chain.ainvoke({
                "category": state["category"],
                "locality": state["locality"],
                "urgency": state["urgency"],
                "text": state["text"],
                "cited": cited
            })
            state["summary"] = result.summary
            return self._trace(state, "summarization", result.reasoning)
        else:
            cited = ", ".join(citation.complaint_id for citation in citations[:3]) or "no prior citations"
            state["summary"] = (
                f"{state['category']} issue in {state['locality']} with {state['urgency']} urgency. "
                f"Grounded against {cited}; recommended action is triage and field verification."
            )
            return self._trace(state, "summarization", "Generated grounded executive summary with retrieved complaint citations.")

    async def _escalation(self, state: ComplaintWorkflowState) -> ComplaintWorkflowState:
        score = state["severity_score"]
        
        if self.llm:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Determine the escalation priority based on the complaint severity score ({score}) and summary. Options: municipal_emergency_cell, department_supervisor, ward_officer."),
                ("human", "Summary: {summary}\nUrgency: {urgency}\nCategory: {category}")
            ])
            chain = prompt | self.llm.with_structured_output(EscalationOutput)
            result = await chain.ainvoke({
                "score": score,
                "summary": state["summary"],
                "urgency": state["urgency"],
                "category": state["category"]
            })
            state["escalation_priority"] = result.escalation_priority
            return self._trace(state, "escalation", result.reasoning)
        else:
            state["escalation_priority"] = "municipal_emergency_cell" if score >= 0.75 else "department_supervisor" if score >= 0.55 else "ward_officer"
            return self._trace(state, "escalation", f"Recommended escalation to {state['escalation_priority']}.")

    def _trace(self, state: ComplaintWorkflowState, agent: str, decision: str) -> ComplaintWorkflowState:
        trace = state.setdefault("reasoning_trace", [])
        trace.append({"agent": agent, "decision": decision})
        return state

