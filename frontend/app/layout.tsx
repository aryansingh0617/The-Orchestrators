import React from "react";
import "./globals.css";
import { Header } from "@/components/ui/Header";

export const metadata = {
  title: "CHIMERA OS | AI Engineering Assessment System",
  description: "Adaptive technical interview operating system evaluating engineering judgment.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen flex flex-col antialiased">
        <Header />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>
        <footer className="border-t border-slate-900 py-4 text-center text-xs text-slate-500">
          Project Chimera — AI Engineering Assessment Operating System
        </footer>
      </body>
    </html>
  );
}
