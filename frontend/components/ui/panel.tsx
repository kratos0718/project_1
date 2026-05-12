import { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export function Panel({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <section className={cn("rounded-lg border border-black/10 bg-white p-5 shadow-panel", className)} {...props} />;
}

