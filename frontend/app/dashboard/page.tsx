import { AppShell } from "@/components/dashboard/shell";
import { OpsDashboard } from "@/components/dashboard/ops-dashboard";
import { fetchAnalytics, fetchComplaints } from "@/lib/api";

export default async function DashboardPage() {
  const [complaints, analytics] = await Promise.all([fetchComplaints(), fetchAnalytics()]);
  return (
    <AppShell>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold">Civic Intelligence Dashboard</h1>
        <p className="mt-1 text-sm text-black/60">Operational view of complaint intake, AI triage, memory, retrieval, and escalation.</p>
      </div>
      <OpsDashboard complaints={complaints} analytics={analytics} />
    </AppShell>
  );
}

