import { AppShell } from "@/components/dashboard/shell";
import { Panel } from "@/components/ui/panel";
import { fetchAnalytics } from "@/lib/api";

export default async function AnalyticsPage() {
  const analytics = await fetchAnalytics();
  return (
    <AppShell>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold">Analytics</h1>
        <p className="mt-1 text-sm text-black/60">Severity, locality, and unresolved issue analytics for civic operators.</p>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <Panel>
          <h2 className="text-lg font-semibold">Locality Heatmap Data</h2>
          <div className="mt-4 space-y-3">
            {Object.entries(analytics.locality_counts).map(([locality, count]) => (
              <div key={locality}>
                <div className="flex justify-between text-sm">
                  <span>{locality}</span>
                  <span>{count}</span>
                </div>
                <div className="mt-1 h-2 rounded-full bg-black/10">
                  <div className="h-2 rounded-full bg-civic" style={{ width: `${Math.min(100, count * 12)}%` }} />
                </div>
              </div>
            ))}
          </div>
        </Panel>
        <Panel>
          <h2 className="text-lg font-semibold">Severity Distribution</h2>
          <div className="mt-4 space-y-3">
            {Object.entries(analytics.severity_distribution).map(([priority, count]) => (
              <div key={priority} className="flex items-center justify-between rounded-md border border-black/10 p-3 text-sm">
                <span>{priority.replaceAll("_", " ")}</span>
                <span className="font-semibold">{count}</span>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </AppShell>
  );
}

