import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AiCRM — AI Customer Platform",
  description: "24/7 AI-powered customer management and booking platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>{children}</body>
    </html>
  );
}
