export default function Loading() {
  return (
    <main className="min-h-screen bg-field p-8">
      <div className="mx-auto max-w-7xl space-y-4">
        <div className="h-8 w-72 animate-pulse rounded-md bg-black/10" />
        <div className="grid gap-4 md:grid-cols-4">
          {[0, 1, 2, 3].map((item) => <div key={item} className="h-32 animate-pulse rounded-lg bg-black/10" />)}
        </div>
      </div>
    </main>
  );
}

