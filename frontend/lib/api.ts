export type Citation = {
  complaint_id: string;
  locality: string;
  category: string;
  score: number;
  excerpt: string;
};

export type AgentReport = {
  summary: string;
  urgency: string;
  severity_score: number;
  escalation_priority: string;
  duplicate_ids: string[];
  citations: Citation[];
  reasoning_trace: Array<{ agent: string; decision: string }>;
};

export type Complaint = {
  id: string;
  raw_text: string;
  cleaned_text: string;
  locality: string;
  category: string;
  status: string;
  severity_score: number | null;
  escalation_priority: string | null;
  created_at: string;
  report?: AgentReport | null;
};

export type Analytics = {
  total_complaints: number;
  open_complaints: number;
  severity_distribution: Record<string, number>;
  locality_counts: Record<string, number>;
  trend_points: Array<Record<string, unknown>>;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function fetchComplaints(): Promise<Complaint[]> {
  const response = await fetch(`${API_BASE}/api/complaints`, { cache: "no-store" });
  if (!response.ok) return [];
  const data = (await response.json()) as { complaints: Complaint[] };
  return data.complaints;
}

export async function fetchAnalytics(): Promise<Analytics> {
  const response = await fetch(`${API_BASE}/api/analytics`, { cache: "no-store" });
  if (!response.ok) {
    return { total_complaints: 0, open_complaints: 0, severity_distribution: {}, locality_counts: {}, trend_points: [] };
  }
  return response.json();
}

export async function submitComplaint(payload: { text: string; locality: string; category: string; metadata: Record<string, unknown> }) {
  const response = await fetch(`${API_BASE}/api/complaints`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error("Complaint submission failed");
  return (await response.json()) as Complaint;
}

