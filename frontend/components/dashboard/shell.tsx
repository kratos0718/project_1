import Link from "next/link";
import { Activity, ClipboardList, Gauge, Network } from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: Gauge },
  { href: "/complaints", label: "Complaints", icon: ClipboardList },
  { href: "/analytics", label: "Analytics", icon: Activity }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-field">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-black/10 bg-ink text-white lg:block">
        <div className="flex h-20 items-center gap-3 px-6">
          <Network className="h-7 w-7 text-[#8dd3c7]" />
          <div>
            <div className="text-sm uppercase tracking-[0.18em] text-white/55">Civic AI</div>
            <div className="font-semibold">Governance Ops</div>
          </div>
        </div>
        <nav className="space-y-1 px-3">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="flex h-11 items-center gap-3 rounded-md px-3 text-sm text-white/80 hover:bg-white/10 hover:text-white">
              <item.icon className="h-4 w-4" />
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="lg:pl-72">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</div>
      </main>
    </div>
  );
}

