"use client";

import { Button } from "@/components/ui/button";

export default function Error({ reset }: { reset: () => void }) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-field p-6">
      <div className="max-w-md rounded-lg border border-black/10 bg-white p-6 shadow-panel">
        <h1 className="text-lg font-semibold">Dashboard failed to load</h1>
        <p className="mt-2 text-sm text-black/60">The platform could not reach one of its services.</p>
        <Button className="mt-4" onClick={reset}>Retry</Button>
      </div>
    </main>
  );
}

