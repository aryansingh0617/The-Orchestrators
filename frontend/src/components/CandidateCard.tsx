'use client';

import React from 'react';
import { Candidate } from '@/lib/candidates';
import { Award, Briefcase, ChevronRight, Zap } from 'lucide-react';

interface CandidateCardProps {
  candidate: Candidate;
  sequenceNum: number;
  onSelect: (candidate: Candidate) => void;
}

export function CandidateCard({ candidate, sequenceNum, onSelect }: CandidateCardProps) {
  const completedMissions = candidate.signals.missionsCompleted;
  const seqFormatted = sequenceNum < 10 ? `0${sequenceNum}` : `${sequenceNum}`;

  return (
    <div
      onClick={() => onSelect(candidate)}
      className="glass-card group cursor-pointer p-6 flex flex-col justify-between select-none relative overflow-hidden"
    >
      <div>
        {/* Header Badge & Sequence Number */}
        <div className="flex items-center justify-between gap-3 mb-4">
          <div className="flex items-center gap-3">
            <span className="w-8 h-8 rounded-full border border-[#C13383]/40 bg-[#443199]/60 flex items-center justify-center font-bitcount text-xs font-normal text-[#C13383]">
              {seqFormatted}
            </span>
            <span className="font-bitcount text-[11px] uppercase tracking-widest text-slate-300 font-normal">
              {candidate.id}
            </span>
          </div>

          <div className="glass-badge px-3 py-1 flex items-center gap-1.5 border border-[#E05454]/40 bg-[#E05454]/15">
            <Award className="w-3.5 h-3.5 text-[#E05454]" />
            <span className="font-bitcount text-xs font-medium text-white">
              {candidate.overallScore} SCORE
            </span>
          </div>
        </div>

        {/* Candidate Header */}
        <div className="flex items-start gap-4 mb-4">
          <div
            className={`w-13 h-13 rounded-xl ${candidate.avatar} flex items-center justify-center font-bold text-white text-lg shadow-md border border-white/30 shrink-0 group-hover:scale-105 transition-transform duration-200`}
          >
            {candidate.name
              .split(' ')
              .map((n) => n[0])
              .join('')}
          </div>

          <div className="min-w-0 flex-1">
            <h3 className="text-base font-normal font-bitcount text-white group-hover:text-[#C13383] transition-colors truncate">
              {candidate.name}
            </h3>
            <p className="text-xs font-normal text-slate-300 truncate mt-0.5 flex items-center gap-1">
              <Briefcase className="w-3 h-3 text-[#E05454] inline shrink-0" />
              {candidate.jobRole}
            </p>
            <div className="flex items-center gap-2 mt-2 font-bitcount text-[10px] text-slate-300">
              <span className="bg-white/10 px-2 py-0.5 rounded border border-white/10">
                {candidate.yearsExperience} YRS EXP
              </span>
              <span className="bg-white/10 px-2 py-0.5 rounded border border-white/10 truncate max-w-[120px]">
                {candidate.education}
              </span>
            </div>
          </div>
        </div>

        {/* Signals Metrics Well */}
        <div className="glass-well p-3 rounded-xl mb-4 space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bitcount text-slate-300 text-[10px] uppercase tracking-wider flex items-center gap-1">
              <Zap className="w-3 h-3 text-[#E05454]" />
              Missions Completed
            </span>
            <span className="font-bitcount font-normal text-[#C13383]">
              {completedMissions} / 31
            </span>
          </div>

          {/* Progress Bar */}
          <div className="w-full h-1.5 bg-slate-950/60 rounded-full overflow-hidden p-0.5 border border-white/10">
            <div
              className="h-full rounded-full bg-gradient-to-r from-[#E05454] to-[#C13383] shadow-[0_0_8px_rgba(224,84,84,0.7)]"
              style={{ width: `${candidate.passRate}%` }}
            />
          </div>
        </div>
      </div>

      {/* Inspect Dossier Action Link */}
      <div className="flex items-center justify-between pt-1 text-xs font-normal font-bitcount text-[#E05454] group-hover:text-[#C13383]">
        <span className="flex items-center gap-1.5">
          Inspect Dossier
        </span>
        <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform text-[#E05454]" />
      </div>
    </div>
  );
}
