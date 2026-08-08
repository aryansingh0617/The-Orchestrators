'use client';

import React from 'react';
import { useParams, useRouter } from 'next/navigation';
import { getCandidateById } from '@/lib/candidates';
import { Reveal } from '@/components/Reveal';
import {
  ArrowLeft,
  FileText,
  Award,
  CheckCircle2,
  TrendingUp,
  Cpu,
  ShieldCheck,
  AlertTriangle,
  Briefcase,
  GraduationCap,
  Sparkles,
} from 'lucide-react';

export default function ReportPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params?.sessionId as string;

  const candidate = getCandidateById(sessionId);

  if (!candidate) {
    return (
      <main className="min-h-screen p-8 flex flex-col items-center justify-center relative z-10 font-bitcount">
        <div className="glass-panel p-8 text-center max-w-md border border-white/25">
          <AlertTriangle className="w-12 h-12 text-[#E05454] mx-auto mb-4" />
          <h1 className="text-xl font-normal text-white font-bitcount">Report Not Found</h1>
          <p className="text-xs text-[#D6D6D6] mt-2 mb-6 font-bitcount">
            No assessment report dossier found for session: {sessionId}
          </p>
          <button
            onClick={() => router.push('/')}
            type="button"
            className="glass-secondary-btn px-4 py-2 text-xs font-bitcount text-[#C13383] font-normal"
          >
            Return to Assessment OS
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen p-4 sm:p-8 max-w-5xl mx-auto relative z-10 font-bitcount space-y-8">
      {/* Navigation Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => router.push('/')}
          type="button"
          className="glass-secondary-btn px-4 py-2.5 flex items-center gap-2 text-xs font-bitcount font-normal text-white cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4 text-[#E05454]" />
          Back to Dossiers
        </button>

        <div className="glass-badge px-4 py-1.5 flex items-center gap-3 border border-[#E05454]/50 bg-[#E05454]/20">
          <FileText className="w-4 h-4 text-[#E05454]" />
          <span className="font-bitcount text-xs font-normal text-white">
            EVALUATION REPORT // {candidate.id}
          </span>
        </div>
      </div>

      {/* Section 1: Executive Summary - Reveal 0ms */}
      <Reveal delayMs={0}>
        <section className="glass-panel p-6 sm:p-8 border border-white/25 relative overflow-hidden">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 pb-6 border-b border-white/20">
            <div className="flex items-center gap-4">
              <div
                className={`w-16 h-16 rounded-2xl ${candidate.avatar} flex items-center justify-center font-bold text-white text-2xl shadow-xl border border-white/40 shrink-0`}
              >
                {candidate.name
                  .split(' ')
                  .map((n) => n[0])
                  .join('')}
              </div>

              <div>
                <h1 className="text-3xl font-light text-white text-glow-coral">
                  {candidate.name}
                </h1>
                <p className="text-xs text-[#D6D6D6] mt-1 flex items-center gap-2 font-normal">
                  <Briefcase className="w-3.5 h-3.5 text-[#E05454]" />
                  {candidate.jobRole} • {candidate.yearsExperience} Yrs Exp
                </p>
                <div className="flex items-center gap-2 text-[11px] text-slate-300 mt-1 font-normal">
                  <GraduationCap className="w-3.5 h-3.5 text-[#C13383]" />
                  {candidate.education}
                </div>
              </div>
            </div>

            <div className="glass-well px-6 py-3 rounded-2xl border border-[#E05454]/50 bg-[#E05454]/20 text-center">
              <div className="text-[10px] uppercase text-[#D6D6D6]">
                Empirical Telemetry Score
              </div>
              <div className="text-3xl font-normal text-white drop-shadow-sm">
                {candidate.overallScore} / 100
              </div>
            </div>
          </div>

          <div className="mt-6 space-y-3">
            <h3 className="text-xs uppercase text-[#E05454] font-normal tracking-wider flex items-center gap-2">
              <ShieldCheck className="w-4 h-4" /> Executive Candidate Assessment Summary
            </h3>
            <p className="text-sm text-[#D6D6D6] leading-relaxed font-light">
              Candidate demonstrated high mastery across Model Context Protocol (MCP) server design, agent tool safety, and asynchronous multi-agent orchestrations. Achieved a first-try resolution accuracy rate of {candidate.firstTryRate}%.
            </p>
          </div>
        </section>
      </Reveal>

      {/* Section 2: Empirical Benchmark Metrics - Reveal 100ms */}
      <Reveal delayMs={100}>
        <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="glass-panel p-5 border border-white/20 text-center">
            <TrendingUp className="w-6 h-6 text-emerald-400 mx-auto mb-2" />
            <div className="text-[10px] uppercase text-[#D6D6D6]">Commit Days Rate</div>
            <div className="text-2xl font-normal text-white mt-1">
              {candidate.signals.commitDays} / 31 Days
            </div>
          </div>

          <div className="glass-panel p-5 border border-white/20 text-center">
            <CheckCircle2 className="w-6 h-6 text-emerald-400 mx-auto mb-2" />
            <div className="text-[10px] uppercase text-[#D6D6D6]">Missions Passed</div>
            <div className="text-2xl font-normal text-white mt-1">
              {candidate.signals.missionsCompleted} / 31 Passed
            </div>
          </div>

          <div className="glass-panel p-5 border border-white/20 text-center">
            <Award className="w-6 h-6 text-[#E05454] mx-auto mb-1" />
            <div className="text-[10px] uppercase text-[#D6D6D6]">1st Try Accuracy</div>
            <div className="text-2xl font-normal text-white mt-1">
              {candidate.signals.missionsFirstTry} ({candidate.firstTryRate}%)
            </div>
          </div>
        </section>
      </Reveal>

      {/* Section 3: AI Recommendations & Technical Skill Matrix - Reveal 200ms */}
      <Reveal delayMs={200}>
        <section className="glass-panel p-6 sm:p-8 border border-white/20 space-y-6">
          <div className="flex items-center gap-2 text-[#E05454]">
            <Cpu className="w-5 h-5" />
            <h3 className="text-base uppercase text-white font-normal">
              Technical Competency Matrix & Recommendations
            </h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="glass-well p-4 rounded-xl space-y-2 border border-white/20">
              <div className="text-xs text-emerald-300 font-normal">
                ✓ Model Context Protocol (MCP) Architecture
              </div>
              <p className="text-xs text-[#D6D6D6]">
                Exemplary JSON-RPC schema definition and timeout safety handlers.
              </p>
            </div>

            <div className="glass-well p-4 rounded-xl space-y-2 border border-white/20">
              <div className="text-xs text-emerald-300 font-normal">
                ✓ Multi-Agent Swarm Orchestration
              </div>
              <p className="text-xs text-[#D6D6D6]">
                Robust task routing and subagent isolation strategies.
              </p>
            </div>

            <div className="glass-well p-4 rounded-xl space-y-2 border border-white/20">
              <div className="text-xs text-amber-300 font-normal">
                ! GPU Memory Allocation under Spikes
              </div>
              <p className="text-xs text-[#D6D6D6]">
                Slight latency under 100+ concurrent LLM inference calls.
              </p>
            </div>

            <div className="glass-well p-4 rounded-xl space-y-2 border border-white/20">
              <div className="text-xs text-emerald-300 font-normal">
                ✓ Code Review & Refactoring Velocity
              </div>
              <p className="text-xs text-[#D6D6D6]">
                Clean modular TypeScript abstractions and strict type enforcement.
              </p>
            </div>
          </div>
        </section>
      </Reveal>

      {/* Section 4: Detailed Mission Log - Reveal 300ms */}
      <Reveal delayMs={300}>
        <section className="glass-panel p-6 sm:p-8 border border-white/20 space-y-4">
          <h3 className="text-sm uppercase text-white font-normal flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-[#C13383]" /> Mission Curriculum Audit Trail ({candidate.missions.length})
          </h3>

          <div className="glass-well p-4 rounded-xl space-y-2.5 max-h-72 overflow-y-auto border border-white/20">
            {candidate.missions.map((m, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between text-xs p-2.5 rounded-lg bg-white/10 border border-white/15"
              >
                <div className="flex items-center gap-3">
                  <span className="text-[10px] text-white bg-white/20 px-2 py-0.5 rounded">
                    DAY {m.day}
                  </span>
                  <span className="text-white font-normal">{m.title}</span>
                </div>
                <span className="text-emerald-300 text-[11px] font-normal">
                  {m.passed ? 'PASSED' : 'SKIPPED'}
                </span>
              </div>
            ))}
          </div>
        </section>
      </Reveal>
    </main>
  );
}
