'use client';

import React from 'react';
import { Candidate } from '@/lib/candidates';
import { Award, Briefcase, Zap, ChevronRight } from 'lucide-react';

interface CandidateCardProps {
  candidate: Candidate;
  onSelect: (candidate: Candidate) => void;
}

export function CandidateCard({ candidate, onSelect }: CandidateCardProps) {
  const completedMissions = candidate.signals.missionsCompleted;
  const firstTryMissions = candidate.signals.missionsFirstTry;
  const commitDays = candidate.signals.commitDays;

  return (
    <div
      onClick={() => onSelect(candidate)}
      className="glass-card group cursor-pointer p-6 flex flex-col justify-between select-none relative overflow-hidden"
    >
      <div>
        {/* Header Badge Strip */}
        <div className="flex items-center justify-between gap-3 mb-4">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" />
            <span className="font-mono text-[11px] uppercase tracking-widest text-slate-300 font-bold">
              {candidate.id}
            </span>
          </div>

          <div className="glass-badge px-3 py-1 flex items-center gap-1.5 border border-amber-400/40 bg-amber-500/15">
            <Award className="w-3.5 h-3.5 text-amber-400" />
            <span className="font-mono text-xs font-black text-amber-300">
              {candidate.overallScore} SCORE
            </span>
          </div>
        </div>

        {/* Candidate Info Header */}
        <div className="flex items-start gap-4 mb-4">
          <div
            className={`w-14 h-14 rounded-2xl ${candidate.avatar} flex items-center justify-center font-black text-white text-xl shadow-lg border border-white/30 shrink-0 group-hover:scale-105 transition-transform duration-200`}
          >
            {candidate.name
              .split(' ')
              .map((n) => n[0])
              .join('')}
          </div>

          <div className="min-w-0 flex-1">
            <h3 className="text-lg font-black text-white group-hover:text-pink-300 transition-colors truncate">
              {candidate.name}
            </h3>
            <p className="text-xs font-semibold text-slate-200 truncate mt-0.5 flex items-center gap-1">
              <Briefcase className="w-3 h-3 text-pink-400 inline shrink-0" />
              {candidate.jobRole}
            </p>
            <div className="flex flex-wrap items-center gap-2 mt-2">
              <span className="text-[10px] font-mono text-slate-200 bg-white/10 px-2 py-0.5 rounded-md border border-white/15">
                {candidate.yearsExperience} YRS EXP
              </span>
              <span className="text-[10px] font-mono text-slate-200 bg-white/10 px-2 py-0.5 rounded-md border border-white/15 truncate max-w-[130px]">
                {candidate.education}
              </span>
            </div>
          </div>
        </div>

        {/* Signals Metrics Well */}
        <div className="glass-well p-3.5 rounded-xl mb-4 space-y-2.5">
          <div className="flex items-center justify-between text-xs">
            <span className="font-mono text-slate-300 text-[10px] uppercase tracking-wider flex items-center gap-1">
              <Zap className="w-3 h-3 text-pink-400" />
              Missions Completed
            </span>
            <span className="font-mono font-bold text-pink-300">
              {completedMissions} / 31 ({candidate.passRate}%)
            </span>
          </div>

          {/* Progress Bar */}
          <div className="w-full h-2 bg-slate-950/70 rounded-full overflow-hidden p-0.5 border border-white/15">
            <div
              className="h-full rounded-full bg-gradient-to-r from-pink-500 via-purple-500 to-amber-500 shadow-[0_0_10px_rgba(236,72,153,0.7)]"
              style={{ width: `${candidate.passRate}%` }}
            />
          </div>

          {/* Signals Breakdown Badges */}
          <div className="grid grid-cols-2 gap-2 pt-1 font-mono text-[11px]">
            <div className="bg-white/10 p-1.5 rounded-lg border border-white/10 flex items-center justify-between">
              <span className="text-slate-300">1st Attempt:</span>
              <span className="font-bold text-emerald-300">{firstTryMissions}</span>
            </div>
            <div className="bg-white/10 p-1.5 rounded-lg border border-white/10 flex items-center justify-between">
              <span className="text-slate-300">Commit Days:</span>
              <span className="font-bold text-violet-300">{commitDays}d</span>
            </div>
          </div>
        </div>
      </div>

      {/* View Dossier Action Link */}
      <div className="flex items-center justify-between pt-1 text-xs font-black text-pink-400 group-hover:text-pink-300">
        <span className="flex items-center gap-1.5">
          Inspect Candidate Dossier
        </span>
        <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform text-pink-400" />
      </div>
    </div>
  );
}
