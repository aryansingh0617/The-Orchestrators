'use client';

import React, { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { getCandidateById } from '@/lib/candidates';
import {
  ArrowLeft,
  Terminal,
  Cpu,
  Award,
  Play,
  Pause,
  CheckCircle2,
  AlertCircle,
  Activity,
  Mic,
  Volume2,
  Briefcase,
  GraduationCap,
  Sparkles,
} from 'lucide-react';

export default function InterviewTerminalPage() {
  const params = useParams();
  const router = useRouter();
  const candidateId = params?.candidateId as string;

  const candidate = getCandidateById(candidateId);

  const [isSimulating, setIsSimulating] = useState(true);
  const [logs, setLogs] = useState<string[]>([
    `[SYS_INIT] Initializing Glassmorphic Assessment Engine...`,
    `[DOSSIER_VERIFIED] Candidate '${candidateId}' telemetry parsed.`,
    `[AGENT_SPAWN] Spawning AI Interviewer Subagent (ID: agent-qa-9)...`,
    `[CURRICULUM_LOAD] Loading Capstone Mission: 'Model Context Protocol & Multi-Agent Swarms'.`,
    `[PROMPT] "Candidate ${candidate?.name || candidateId}, demonstrate how your MCP server architecture handles tool timeouts under load."`,
  ]);

  if (!candidate) {
    return (
      <main className="min-h-screen p-8 flex flex-col items-center justify-center relative z-10">
        <div className="glass-panel p-8 text-center max-w-md border border-white/10">
          <AlertCircle className="w-12 h-12 text-amber-400 mx-auto mb-4" />
          <h1 className="text-xl font-bold text-white">Candidate Not Found</h1>
          <p className="text-xs text-slate-400 mt-2 mb-6">
            No candidate dossier found with ID: {candidateId}
          </p>
          <button
            onClick={() => router.push('/')}
            type="button"
            className="glass-secondary-btn px-4 py-2 text-xs font-mono text-cyan-300 font-bold"
          >
            Return to Assessment OS
          </button>
        </div>
      </main>
    );
  }

  const handleSimulateNextStep = () => {
    const nextLogs = [
      `[RESPONSE_EVAL] Candidate provided asynchronous JSON-RPC protocol definition with schema validation.`,
      `[BENCHMARK] Automated MCP tool call suite executed... Result: 100% Pass.`,
      `[SIGNAL_GEN] Telemetry score updated (+4.2 pts for Agentic Architecture).`,
    ];
    setLogs((prev) => [...prev, ...nextLogs]);
  };

  return (
    <main className="min-h-screen p-4 sm:p-8 max-w-7xl mx-auto relative z-10">
      {/* Navigation Header */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={() => router.push('/')}
          type="button"
          className="glass-secondary-btn px-4 py-2.5 flex items-center gap-2 text-xs font-mono font-bold text-slate-200 cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4 text-cyan-400" />
          Back to Dossiers
        </button>

        <div className="glass-badge px-4 py-1.5 flex items-center gap-3 border border-cyan-400/30 bg-cyan-500/10">
          <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping" />
          <span className="font-mono text-xs font-bold text-cyan-200">
            SIMULATION ROOM // {candidate.id}
          </span>
        </div>
      </div>

      {/* Main Glass Terminal Frame */}
      <div className="glass-panel p-6 sm:p-8 mb-6 border border-white/20 relative overflow-hidden">
        {/* Ambient Glows */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Candidate Profile Bar */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6 pb-6 border-b border-white/10 relative z-10">
          <div className="flex items-center gap-4">
            <div
              className={`w-14 h-14 rounded-2xl ${candidate.avatar} flex items-center justify-center font-black text-white text-xl shadow-lg border border-white/30 shrink-0`}
            >
              {candidate.name
                .split(' ')
                .map((n) => n[0])
                .join('')}
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-black text-white glass-text-glow">
                  {candidate.name}
                </h1>
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                  {candidate.id}
                </span>
              </div>
              <p className="text-xs font-medium text-cyan-300 mt-1 flex items-center gap-2">
                <Briefcase className="w-3.5 h-3.5" />
                {candidate.jobRole} • {candidate.yearsExperience} Yrs Exp • {candidate.education}
              </p>
            </div>
          </div>

          <div className="glass-well px-5 py-2.5 rounded-2xl border border-amber-400/30 bg-amber-500/10 flex items-center gap-3 self-stretch md:self-auto justify-center">
            <Award className="w-6 h-6 text-amber-400 shrink-0" />
            <div>
              <div className="text-[10px] font-mono uppercase text-slate-400">
                OVERALL RATING
              </div>
              <div className="text-xl font-mono font-black text-amber-300">
                {candidate.overallScore} / 100
              </div>
            </div>
          </div>
        </div>

        {/* Terminal Screen & Controller */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10">
          {/* Terminal Output */}
          <div className="lg:col-span-2 flex flex-col justify-between">
            <div className="flex items-center justify-between font-mono text-xs text-slate-300 mb-2">
              <span className="flex items-center gap-2 font-bold">
                <Terminal className="w-4 h-4 text-cyan-400" />
                REAL-TIME AGENT INTERVIEW STREAM
              </span>
              <span className="text-emerald-400 flex items-center gap-1.5 font-bold">
                <Activity className="w-3.5 h-3.5 animate-pulse" />
                STREAMING
              </span>
            </div>

            <div className="glass-well rounded-2xl p-4 font-mono text-xs text-slate-200 h-80 overflow-y-auto space-y-2 border border-white/10 shadow-inner">
              {logs.map((log, idx) => (
                <div
                  key={idx}
                  className={`leading-relaxed ${
                    log.includes('[SYS')
                      ? 'text-slate-400'
                      : log.includes('[PROMPT]')
                      ? 'text-cyan-300 font-bold bg-cyan-500/10 p-2 rounded-lg border border-cyan-500/20'
                      : log.includes('[BENCHMARK]')
                      ? 'text-emerald-400'
                      : 'text-slate-200'
                  }`}
                >
                  {log}
                </div>
              ))}
            </div>

            {/* Simulation Control Buttons */}
            <div className="flex items-center gap-3 mt-4">
              <button
                onClick={handleSimulateNextStep}
                type="button"
                className="glass-secondary-btn px-4 py-2.5 flex items-center gap-2 text-xs font-mono font-bold text-cyan-300 cursor-pointer"
              >
                <Play className="w-4 h-4 fill-cyan-300" />
                Step Next Prompt
              </button>
              <button
                onClick={() => setIsSimulating(!isSimulating)}
                type="button"
                className="glass-secondary-btn px-4 py-2.5 flex items-center gap-2 text-xs font-mono font-bold text-slate-300 cursor-pointer"
              >
                {isSimulating ? <Pause className="w-4 h-4 text-amber-400" /> : <Play className="w-4 h-4 text-emerald-400" />}
                {isSimulating ? 'Pause Stream' : 'Resume Stream'}
              </button>
            </div>
          </div>

          {/* Side Evaluation Metrics Panel */}
          <div className="space-y-4">
            <div className="glass-well rounded-2xl p-4 border border-white/10">
              <h3 className="font-mono text-xs font-bold text-slate-200 uppercase mb-3 flex items-center gap-2">
                <Cpu className="w-4 h-4 text-cyan-400" />
                Active Evaluation Module
              </h3>
              <div className="bg-white/5 p-3.5 rounded-xl border border-white/10 space-y-2">
                <div className="font-bold text-xs text-white">
                  Model Context Protocol (MCP) & Agents
                </div>
                <p className="text-[11px] text-slate-300 leading-relaxed">
                  Evaluating tool schema design, function execution safety, and error handling.
                </p>
                <div className="pt-2 flex items-center justify-between text-[11px] font-mono border-t border-white/10">
                  <span className="text-slate-400">Status:</span>
                  <span className="text-emerald-400 font-bold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> EVALUATING
                  </span>
                </div>
              </div>
            </div>

            {/* Audio Synthesis Hardware Box */}
            <div className="glass-well rounded-2xl p-4 border border-white/10">
              <h3 className="font-mono text-xs font-bold text-slate-200 uppercase mb-3 flex items-center gap-2">
                <Mic className="w-4 h-4 text-cyan-400" />
                Neural Audio Synthesizer
              </h3>
              <div className="flex items-center justify-between text-xs font-mono text-slate-200 bg-white/5 p-3 rounded-xl border border-white/10">
                <div className="flex items-center gap-2">
                  <Volume2 className="w-4 h-4 text-emerald-400 animate-pulse" />
                  <span>Real-time Voice Engine</span>
                </div>
                <span className="text-[10px] text-emerald-400 font-bold bg-emerald-500/20 px-2 py-0.5 rounded-full border border-emerald-500/30">
                  ACTIVE
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
