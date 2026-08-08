'use client';

import React from 'react';
import { Search, ChevronLeft, ChevronRight, Cpu } from 'lucide-react';

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
  onPrevCandidate?: () => void;
  onNextCandidate?: () => void;
}

export function HeroSection({
  searchQuery,
  onSearchChange,
  selectedFilter,
  onFilterChange,
  totalCandidates,
  cohortInfo,
  onPrevCandidate,
  onNextCandidate,
}: HeroSectionProps) {
  const filters = [
    { id: 'ALL', label: 'All' },
    { id: 'TOP_PERFORMER', label: 'Top' },
    { id: 'HIGH_ACCURACY', label: 'Accuracy' },
    { id: 'HIGH_CONSISTENCY', label: 'Consistency' },
  ];

  return (
    <header className="mb-10 relative z-10">
      {/* Minimal Top Navbar */}
      <nav className="flex items-center justify-between py-4 mb-8 border-b border-[#C13383]/25">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full border border-[#C13383]/40 bg-[#443199]/60 flex items-center justify-center shadow-sm">
            <Cpu className="w-4 h-4 text-[#E05454]" />
          </div>
          <span className="font-bitcount text-lg font-light tracking-widest text-white">
            CHIMERA OS
          </span>
        </div>

        {/* Sparse Nav Links */}
        <div className="flex items-center gap-6 sm:gap-8 font-bitcount text-xs text-white/90 font-normal">
          <a href="#missions" className="hover:text-[#C13383] transition-colors">
            Missions
          </a>
          <a href="#profile" className="hover:text-[#C13383] transition-colors">
            Profile
          </a>
          <a href="#system" className="hover:text-[#C13383] transition-colors">
            System
          </a>
        </div>
      </nav>

      {/* Main Hero Container */}
      <div className="glass-panel p-6 sm:p-10 mb-6 relative overflow-hidden">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8 relative z-10">
          <div className="space-y-4 max-w-2xl">
            {/* Sequence Indicator & Pill */}
            <div className="flex items-center gap-4">
              <div className="w-11 h-11 rounded-full border-2 border-[#C13383]/60 bg-[#443199]/50 flex items-center justify-center font-bitcount text-base font-medium text-[#C13383] shadow-inner">
                01
              </div>
              <div className="glass-badge px-3.5 py-1 flex items-center gap-2 border border-[#E05454]/40 bg-[#E05454]/15">
                <span className="w-2 h-2 rounded-full bg-[#E05454] animate-pulse" />
                <span className="font-bitcount text-xs font-normal text-white tracking-wider">
                  AI COHORT // {totalCandidates} DOSSIERS
                </span>
              </div>
            </div>

            {/* Main CHIMERA Hero Logo Text - Significantly Less Bold (font-light / font-normal) */}
            <h1 className="font-bitcount text-5xl sm:text-7xl font-light tracking-tight text-glow-coral leading-none">
              CHIMERA
            </h1>

            {/* Concise Minimal Copy (Max 1-2 Short Sentences) */}
            <p className="text-sm sm:text-base text-slate-100 font-light leading-relaxed max-w-lg">
              Empirical AI engineering assessment platform. Benchmarking candidate telemetry across 31 missions and multi-agent workflows.
            </p>
          </div>

          {/* Controls: Circular Navigation Arrows (← →) */}
          <div className="flex flex-col sm:flex-row items-center gap-4 self-stretch md:self-auto justify-end">
            <div className="flex items-center gap-3">
              <button
                onClick={onPrevCandidate}
                type="button"
                aria-label="Previous Candidate"
                className="w-12 h-12 rounded-full border border-[#C13383]/40 bg-[#443199]/50 backdrop-blur-md flex items-center justify-center text-white hover:border-[#E05454] hover:bg-[#E05454]/20 transition-all cursor-pointer shadow-md"
              >
                <ChevronLeft className="w-6 h-6 text-white" />
              </button>
              <button
                onClick={onNextCandidate}
                type="button"
                aria-label="Next Candidate"
                className="w-12 h-12 rounded-full border border-[#C13383]/40 bg-[#443199]/50 backdrop-blur-md flex items-center justify-center text-white hover:border-[#E05454] hover:bg-[#E05454]/20 transition-all cursor-pointer shadow-md"
              >
                <ChevronRight className="w-6 h-6 text-white" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Minimal Filter Controls & Search */}
      <div className="glass-panel p-3.5 flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Search Bar */}
        <div className="relative w-full sm:w-72">
          <div className="glass-well rounded-xl flex items-center px-3.5 py-2 border border-[#C13383]/25 focus-within:border-[#E05454]/60 transition-colors">
            <Search className="w-4 h-4 text-slate-300 shrink-0 mr-2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder="Search candidate..."
              className="bg-transparent text-xs text-white placeholder-slate-400 focus:outline-none w-full font-bitcount font-normal"
            />
          </div>
        </div>

        {/* Sparse Filter Buttons */}
        <div className="flex items-center gap-2 w-full sm:w-auto">
          {filters.map((f) => {
            const isActive = selectedFilter === f.id;
            return (
              <button
                key={f.id}
                onClick={() => onFilterChange(f.id)}
                type="button"
                className={`glass-secondary-btn text-xs font-normal px-3 py-1.5 font-bitcount cursor-pointer ${
                  isActive ? 'active text-[#E05454]' : 'text-white'
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
