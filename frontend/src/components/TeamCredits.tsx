"use client";

import React, { useState } from "react";
import { Users, ChevronDown, ChevronUp, Code2, Cpu, ShieldCheck } from "lucide-react";

export function TeamCredits() {
  const [isExpanded, setIsExpanded] = useState<boolean>(true);

  return (
    <aside
      aria-label="Team Credits"
      className="fixed bottom-3 right-3 z-50 font-bitcount transition-all duration-300 pointer-events-auto select-none"
    >
      <div className="bg-[#130A24]/90 backdrop-blur-md border border-[#E05454]/30 hover:border-[#C13383]/60 rounded-2xl p-3 text-[11px] shadow-2xl max-w-xs text-slate-200">
        {/* Badge Header Bar */}
        <div
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center justify-between gap-3 cursor-pointer pb-1 border-b border-white/10"
        >
          <div className="flex items-center gap-2">
            <Users className="w-3.5 h-3.5 text-[#E05454] animate-pulse" />
            <span className="font-semibold text-white uppercase tracking-wider text-[10px] text-glow-coral">
              THE ORCHESTRATORS
            </span>
          </div>

          <button
            type="button"
            className="text-slate-400 hover:text-white p-0.5 rounded-lg transition-colors"
          >
            {isExpanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronUp className="w-3.5 h-3.5" />}
          </button>
        </div>

        {/* Expandable Team List */}
        {isExpanded && (
          <div className="mt-2.5 space-y-2 font-bitcount text-[11px]">
            <div className="flex items-start gap-2">
              <Code2 className="w-3 h-3 text-[#E05454] shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold text-white">Dhruv Sharma</span>
                <span className="text-slate-400 block text-[10px] leading-tight">
                  frontend, api and deployment
                </span>
              </div>
            </div>

            <div className="flex items-start gap-2">
              <Cpu className="w-3 h-3 text-[#C13383] shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold text-white">Aryan Singh</span>
                <span className="text-slate-400 block text-[10px] leading-tight">
                  frontend and backend pipelines
                </span>
              </div>
            </div>

            <div className="flex items-start gap-2">
              <ShieldCheck className="w-3 h-3 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold text-white">Sujal Singh Negi</span>
                <span className="text-slate-400 block text-[10px] leading-tight">
                  overall project management
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}
