'use client';

import React, { useEffect } from 'react';
import { Candidate } from '@/lib/candidates';
import { TactileButton } from './TactileButton';
import {
  X,
  Award,
  CheckCircle2,
  AlertTriangle,
  Briefcase,
  GraduationCap,
  Layers,
} from 'lucide-react';

interface CandidateModalProps {
  candidate: Candidate | null;
  onClose: () => void;
}

export function CandidateModal({ candidate, onClose }: CandidateModalProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!candidate) return null;

  const passedMissions = candidate.passedMissions;
  const skippedMissions = candidate.skippedMissions;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-in fade-in duration-200">
      {/* Dark Blur Backdrop */}
      <div
        onClick={onClose}
        className="fixed inset-0 bg-[#412653]/80 backdrop-blur-xl transition-opacity"
      />

      {/* Glassmorphic Modal Frame */}
      <div className="glass-modal relative w-full max-w-3xl z-10 p-6 sm:p-8 max-h-[90vh] overflow-y-auto my-auto border border-[#D174D2]/40 shadow-[0_35px_90px_rgba(0,0,0,0.9)]">
        {/* Close Button */}
        <button
          onClick={onClose}
          type="button"
          className="glass-secondary-btn absolute top-5 right-5 w-9 h-9 rounded-full flex items-center justify-center text-white hover:text-[#E0563F] z-20 cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Top Header Badge */}
        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-white/15">
          <div className="glass-badge px-3.5 py-1 flex items-center gap-2 border border-[#E0563F]/40 bg-[#E0563F]/15">
            <span className="w-2 h-2 rounded-full bg-[#E0563F] animate-pulse" />
            <span className="font-mono text-xs font-bold text-white uppercase tracking-widest">
              CHIMERA DOSSIER // {candidate.id}
            </span>
          </div>
        </div>

        {/* Candidate Profile Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-4">
            <div
              className={`w-16 h-16 rounded-2xl ${candidate.avatar} flex items-center justify-center font-black text-white text-2xl shadow-xl border border-white/40 shrink-0`}
            >
              {candidate.name
                .split(' ')
                .map((n) => n[0])
                .join('')}
            </div>

            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-2xl sm:text-3xl font-bold font-bitcount text-white text-glow-coral">
                  {candidate.name}
                </h2>
                <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  {candidate.status}
                </span>
              </div>
              <p className="text-sm font-semibold text-[#D174D2] mt-1 flex items-center gap-1.5">
                <Briefcase className="w-4 h-4 text-[#E0563F]" />
                {candidate.jobRole}
              </p>
              <div className="flex flex-wrap items-center gap-3 text-xs font-mono text-slate-200 mt-1.5">
                <span>{candidate.yearsExperience} Yrs Experience</span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <GraduationCap className="w-3.5 h-3.5 text-[#D174D2]" />
                  {candidate.education}
                </span>
              </div>
            </div>
          </div>

          {/* Assessment Score Badge */}
          <div className="glass-well p-4 rounded-2xl border border-[#E0563F]/40 bg-[#E0563F]/15 flex items-center gap-3 self-stretch sm:self-auto justify-center">
            <Award className="w-8 h-8 text-[#E0563F] shrink-0" />
            <div>
              <div className="text-[10px] font-mono uppercase text-slate-300">
                RATING
              </div>
              <div className="text-2xl font-black font-mono text-white">
                {candidate.overallScore} / 100
              </div>
            </div>
          </div>
        </div>

        {/* Signals Overview Grid */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          <div className="glass-well p-3.5 rounded-xl text-center border border-white/15">
            <div className="text-[10px] font-mono text-slate-300 uppercase mb-1">
              Commit Days
            </div>
            <div className="text-lg font-black font-mono text-[#D174D2]">
              {candidate.signals.commitDays} / 31
            </div>
          </div>
          <div className="glass-well p-3.5 rounded-xl text-center border border-white/15">
            <div className="text-[10px] font-mono text-slate-300 uppercase mb-1">
              Missions Passed
            </div>
            <div className="text-lg font-black font-mono text-emerald-300">
              {candidate.signals.missionsCompleted} / 31
            </div>
          </div>
          <div className="glass-well p-3.5 rounded-xl text-center border border-white/15">
            <div className="text-[10px] font-mono text-slate-300 uppercase mb-1">
              1st Try Accuracy
            </div>
            <div className="text-lg font-black font-mono text-[#E0563F]">
              {candidate.signals.missionsFirstTry} ({candidate.firstTryRate}%)
            </div>
          </div>
        </div>

        {/* Missions Breakdown List */}
        <div className="mb-8">
          <div className="flex items-center justify-between font-mono text-xs font-bold text-slate-200 uppercase mb-3">
            <span className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-[#E0563F]" />
              Evaluated Curriculum Missions Log ({candidate.missions.length})
            </span>
            <span className="text-slate-300 text-[11px]">
              {passedMissions.length} Passed • {skippedMissions.length} Skipped
            </span>
          </div>

          <div className="glass-well rounded-xl p-4 space-y-2.5 max-h-64 overflow-y-auto border border-white/15">
            {candidate.missions.map((m, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between text-xs p-2.5 rounded-lg bg-white/10 border border-white/10 hover:border-white/20 transition-colors"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <span className="font-mono text-[10px] font-bold text-slate-200 bg-white/15 px-2 py-0.5 rounded shrink-0">
                    DAY {m.day}
                  </span>
                  <span className="font-semibold text-slate-100 truncate">
                    {m.title}
                  </span>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  {m.passed && (
                    <span className="flex items-center gap-1 text-[11px] font-mono font-bold text-emerald-400 bg-emerald-500/20 px-2 py-0.5 rounded border border-emerald-500/30">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      PASSED ({m.attempts || 1} {m.attempts === 1 ? 'try' : 'tries'})
                    </span>
                  )}
                  {m.skipped && (
                    <span className="flex items-center gap-1 text-[11px] font-mono font-bold text-amber-400 bg-amber-500/20 px-2 py-0.5 rounded border border-amber-500/30">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      SKIPPED
                    </span>
                  )}
                  {!m.passed && !m.skipped && (
                    <span className="flex items-center gap-1 text-[11px] font-mono font-bold text-rose-400 bg-rose-500/20 px-2 py-0.5 rounded border border-rose-500/30">
                      FAILED ({m.attempts} tries)
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Massive Glassmorphic Action Push Button */}
        <div className="pt-2 border-t border-white/15 text-center">
          <p className="text-xs font-mono text-slate-300 uppercase tracking-widest mb-4">
            Initialize AI Candidate Assessment Simulation
          </p>
          <TactileButton candidateId={candidate.id} size="xl" />
        </div>
      </div>
    </div>
  );
}
