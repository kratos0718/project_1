from langgraph.graph import END, StateGraph

from app.agents.state import ComplaintWorkflowState
from app.models.schemas import AgentReport


class ComplaintAgentWorkflow:
    def __init__(self) -> None:
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
        text = state["text"].lower()
        severe_terms = {"fire", "sewage", "collapse", "accident", "flood", "contamination", "hospital", "school"}
        score = min(1.0, 0.25 + sum(0.12 for term in severe_terms if term in text))
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
        cited = ", ".join(citation.complaint_id for citation in state.get("citations", [])[:3]) or "no prior citations"
        state["summary"] = (
            f"{state['category']} issue in {state['locality']} with {state['urgency']} urgency. "
            f"Grounded against {cited}; recommended action is triage and field verification."
        )
        return self._trace(state, "summarization", "Generated grounded executive summary with retrieved complaint citations.")

    async def _escalation(self, state: ComplaintWorkflowState) -> ComplaintWorkflowState:
        score = state["severity_score"]
        state["escalation_priority"] = "municipal_emergency_cell" if score >= 0.75 else "department_supervisor" if score >= 0.55 else "ward_officer"
        return self._trace(state, "escalation", f"Recommended escalation to {state['escalation_priority']}.")

    def _trace(self, state: ComplaintWorkflowState, agent: str, decision: str) -> ComplaintWorkflowState:
        trace = state.setdefault("reasoning_trace", [])
        trace.append({"agent": agent, "decision": decision})
        return state

