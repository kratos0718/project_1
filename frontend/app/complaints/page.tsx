import { ComplaintForm } from "@/components/dashboard/complaint-form";
import { AppShell } from "@/components/dashboard/shell";
import { Panel } from "@/components/ui/panel";

export default function ComplaintsPage() {
  return (
    <AppShell>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold">Complaint Intake</h1>
        <p className="mt-1 text-sm text-black/60">Submissions are embedded, retrieved against history, scored by agents, and persisted to memory.</p>
      </div>
      <Panel>
        <ComplaintForm />
      </Panel>
    </AppShell>
  );
}

