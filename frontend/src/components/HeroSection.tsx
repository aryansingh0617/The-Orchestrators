'use client';

import React from 'react';
import { Cpu, Search, Filter, ShieldCheck, Sparkles, Flame } from 'lucide-react';

interface HeroSectionProps {
  searchQuery: string;
  onSearchChange: (q: string) => void;
  selectedFilter: string;
  onFilterChange: (filter: string) => void;
  totalCandidates: number;
  cohortInfo: {
    cohort: string;
    modulesCount: number;
    daysCount: number;
  };
}

export function HeroSection({
  searchQuery,
  onSearchChange,
  selectedFilter,
  onFilterChange,
  totalCandidates,
  cohortInfo,
}: HeroSectionProps) {
  const filters = [
    { id: 'ALL', label: 'All Dossiers' },
    { id: 'TOP_PERFORMER', label: 'Top Performers' },
    { id: 'HIGH_ACCURACY', label: 'High 1st-Try Rate' },
    { id: 'HIGH_CONSISTENCY', label: '25+ Commit Days' },
  ];

  return (
    <header className="mb-10 relative z-10">
      {/* Top Frosted Glass Panel */}
      <div className="glass-panel p-6 sm:p-10 mb-8 relative overflow-hidden">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8 relative z-10">
          <div className="space-y-4 max-w-2xl">
            {/* Status Pills */}
            <div className="flex flex-wrap items-center gap-3">
              <div className="glass-badge px-3.5 py-1 flex items-center gap-2 border border-pink-400/30 bg-pink-500/10">
                <span className="w-2 h-2 rounded-full bg-pink-400 animate-pulse" />
                <span className="font-mono text-xs font-bold text-pink-200 tracking-wider">
                  {cohortInfo.cohort.toUpperCase()}
                </span>
              </div>
              <div className="flex items-center gap-2 font-mono text-xs text-slate-200 bg-white/10 px-3.5 py-1 rounded-full border border-white/20">
                <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                <span>{totalCandidates} CANDIDATES ASSESSED</span>
              </div>
            </div>

            {/* Title with Glass Glow */}
            <h1 className="text-4xl sm:text-6xl font-black tracking-tight glass-text-glow flex items-center gap-3">
              <Cpu className="w-10 h-10 sm:w-14 sm:h-14 text-pink-400 drop-shadow-[0_0_25px_rgba(236,72,153,0.7)] shrink-0" />
              CHIMERA
            </h1>

            {/* Description */}
            <p className="text-sm sm:text-base text-slate-200 leading-relaxed font-normal max-w-xl">
              <strong className="text-white font-semibold">AI Engineering Assessment OS</strong> — High-fidelity frosted telemetry analytics evaluating engineering candidates across 31 missions, vector search, multi-agent orchestration, and MCP integration.
            </p>
          </div>

          {/* Metrics Glass Box */}
          <div className="glass-well p-5 rounded-2xl self-stretch md:self-auto min-w-[240px] flex flex-col justify-between border border-white/15">
            <div className="flex items-center justify-between text-xs font-mono text-slate-300 mb-3 border-b border-white/10 pb-2">
              <span className="flex items-center gap-1.5 font-bold text-white">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                COHORT TELEMETRY
              </span>
            </div>

            <div className="space-y-2.5 font-mono text-xs">
              <div className="flex justify-between items-center">
                <span className="text-slate-300">Total Modules:</span>
                <span className="font-extrabold text-pink-300">{cohortInfo.modulesCount} Modules</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-300">Total Curriculum:</span>
                <span className="font-extrabold text-violet-300">{cohortInfo.daysCount} Days</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-300">Evaluation Engine:</span>
                <span className="font-extrabold text-emerald-400 flex items-center gap-1">
                  <Flame className="w-3.5 h-3.5 text-amber-400 fill-amber-400" /> LIVE
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Glass Filter Controls */}
      <div className="glass-panel p-4 flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Search Bar */}
        <div className="relative w-full md:w-80">
          <div className="glass-well rounded-xl flex items-center px-3.5 py-2.5 border border-white/15 focus-within:border-pink-400/60 transition-colors">
            <Search className="w-4 h-4 text-slate-300 shrink-0 mr-2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder="Search candidate name or role..."
              className="bg-transparent text-xs sm:text-sm text-white placeholder-slate-400 focus:outline-none w-full font-mono"
            />
          </div>
        </div>

        {/* Filter Buttons */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          <span className="text-xs font-mono text-slate-300 flex items-center gap-1 mr-1 hidden sm:flex">
            <Filter className="w-3.5 h-3.5 text-pink-400" />
            FILTER:
          </span>
          {filters.map((f) => {
            const isActive = selectedFilter === f.id;
            return (
              <button
                key={f.id}
                onClick={() => onFilterChange(f.id)}
                type="button"
                className={`glass-secondary-btn text-xs font-bold px-3.5 py-2 font-mono tracking-wider cursor-pointer ${
                  isActive ? 'active text-pink-300' : 'text-slate-200'
                }`}
              >
                {f.label}
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
