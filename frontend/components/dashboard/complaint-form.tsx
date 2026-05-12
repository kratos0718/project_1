"use client";

import { useState, useTransition } from "react";
import { Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { submitComplaint, type Complaint } from "@/lib/api";

export function ComplaintForm({ onCreated }: { onCreated?: (complaint: Complaint) => void }) {
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);
  const [text, setText] = useState("");
  const [locality, setLocality] = useState("");
  const [category, setCategory] = useState("sanitation");

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    startTransition(async () => {
      try {
        const complaint = await submitComplaint({ text, locality, category, metadata: { source: "web" } });
        setText("");
        onCreated?.(complaint);
      } catch {
        setError("Unable to submit complaint. Confirm the backend is running and configured.");
      }
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid gap-3 md:grid-cols-2">
        <input className="h-10 rounded-md border border-black/15 px-3 text-sm" placeholder="Locality" value={locality} onChange={(event) => setLocality(event.target.value)} required />
        <select className="h-10 rounded-md border border-black/15 px-3 text-sm" value={category} onChange={(event) => setCategory(event.target.value)}>
          <option value="sanitation">Sanitation</option>
          <option value="roads">Roads</option>
          <option value="water">Water</option>
          <option value="safety">Public safety</option>
          <option value="electricity">Electricity</option>
        </select>
      </div>
      <textarea
        className="min-h-36 w-full rounded-md border border-black/15 p-3 text-sm leading-6"
        placeholder="Describe the civic issue, impact, location markers, and urgency signals..."
        value={text}
        onChange={(event) => setText(event.target.value)}
        required
      />
      {error ? <div className="rounded-md bg-red-50 p-3 text-sm text-danger">{error}</div> : null}
      <Button disabled={isPending || text.length < 20 || locality.length < 2}>
        <Send className="h-4 w-4" />
        {isPending ? "Analyzing" : "Submit complaint"}
      </Button>
    </form>
  );
}

