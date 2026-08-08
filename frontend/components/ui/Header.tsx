import React from "react";
import Link from "next/link";
import { Terminal, Shield, Cpu, Activity } from "lucide-react";

export function Header() {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-sky-500/10 border border-sky-500/30 text-sky-400">
            <Cpu className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <span className="font-bold text-lg tracking-wider text-slate-100 uppercase">
              CHIMERA <span className="text-sky-400 font-mono text-sm">OS</span>
            </span>
            <p className="text-xs text-slate-400 hidden sm:block">AI Engineering Assessment Engine</p>
          </div>
        </div>

        <nav className="flex items-center space-x-6 text-sm font-medium">
          <Link href="/" className="text-slate-300 hover:text-sky-400 transition-colors flex items-center gap-1.5">
            <Terminal className="w-4 h-4" /> Assessment
          </Link>
          <Link href="/sessions" className="text-slate-300 hover:text-sky-400 transition-colors flex items-center gap-1.5">
            <Activity className="w-4 h-4" /> Sessions
          </Link>
          <Link href="/reports" className="text-slate-300 hover:text-sky-400 transition-colors flex items-center gap-1.5">
            <Shield className="w-4 h-4" /> Reports
          </Link>
        </nav>
      </div>
    </header>
  );
}
