import type { Metadata } from "next";
// @ts-ignore: CSS module import for Next.js global stylesheet
import "./globals.css";

export const metadata: Metadata = {
  title: "OpportunityRadar",
  description: "Job search agent with visa-sponsorship scoring and resume tailoring",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen">{children}</body>
    </html>
  );
}
