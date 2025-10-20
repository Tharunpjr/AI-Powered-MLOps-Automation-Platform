import type { Metadata } from "next";
import "./globals.css";
import VisualEditsMessenger from "../visual-edits/VisualEditsMessenger";
import ErrorReporter from "@/components/ErrorReporter";

export const metadata: Metadata = {
  title: "AutoOps - AI-Powered MLOps Platform",
  description: "Complete AI Platform - Traditional ML, Deep Learning & LLMs",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
        <VisualEditsMessenger />
        <ErrorReporter />
      </body>
    </html>
  );
}