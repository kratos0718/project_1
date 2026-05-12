import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Civic Intelligence Platform",
  description: "Multi-agent AI platform for civic complaint intelligence"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

