import { AlertTriangle, BrainCircuit, GitBranch, MapPinned } from "lucide-react";
import { Panel } from "@/components/ui/panel";
import { type Analytics, type Complaint } from "@/lib/api";

export function OpsDashboard({ complaints, analytics }: { complaints: Complaint[]; analytics: Analytics }) {
  const latest = complaints[0];
  const stats = [
    { label: "Total complaints", value: analytics.total_complaints, icon: GitBranch },
    { label: "Open issues", value: analytics.open_complaints, icon: AlertTriangle },
    { label: "Localities", value: Object.keys(analytics.locality_counts).length, icon: MapPinned },
    { label: "Reasoned cases", value: complaints.filter((item) => item.severity_score !== null).length, icon: BrainCircuit }
  ];

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-4">
        {stats.map((stat) => (
          <Panel key={stat.label}>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-black/55">{stat.label}</div>
                <div className="mt-2 text-3xl font-semibold">{stat.value}</div>
              </div>
              <stat.icon className="h-6 w-6 text-civic" />
            </div>
          </Panel>
        ))}
      </div>
      <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        <Panel>
          <h2 className="text-lg font-semibold">Complaint Feed</h2>
          <div className="mt-4 divide-y divide-black/10">
            {complaints.slice(0, 6).map((complaint) => (
              <article key={complaint.id} className="py-4">
                <div className="flex flex-wrap items-center gap-2 text-xs text-black/55">
                  <span>{complaint.locality}</span>
                  <span>{complaint.category}</span>
                  <span>{complaint.escalation_priority ?? "pending"}</span>
                </div>
                <p className="mt-2 text-sm leading-6">{complaint.cleaned_text}</p>
              </article>
            ))}
            {complaints.length === 0 ? <p className="py-8 text-sm text-black/55">No complaints submitted yet.</p> : null}
          </div>
        </Panel>
        <Panel>
          <h2 className="text-lg font-semibold">AI Reasoning Trace</h2>
          <div className="mt-4 space-y-3">
            {latest?.report?.reasoning_trace.map((step) => (
              <div key={`${step.agent}-${step.decision}`} className="rounded-md border border-black/10 p-3">
                <div className="text-sm font-semibold capitalize">{step.agent.replaceAll("_", " ")}</div>
                <p className="mt-1 text-sm leading-6 text-black/65">{step.decision}</p>
              </div>
            )) ?? <p className="text-sm text-black/55">Submit a complaint to inspect agent decisions.</p>}
          </div>
        </Panel>
      </div>
    </div>
  );
}

