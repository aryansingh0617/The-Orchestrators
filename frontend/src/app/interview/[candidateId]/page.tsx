'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { getCandidateById } from '@/lib/candidates';
import {
  ArrowLeft,
  Terminal,
  Cpu,
  Award,
  CheckCircle2,
  AlertCircle,
  Activity,
  Mic,
  Volume2,
  Briefcase,
  Send,
  Loader2,
} from 'lucide-react';

export default function InterviewTerminalPage() {
  const params = useParams();
  const router = useRouter();
  const candidateId = params?.candidateId as string;

  const candidate = getCandidateById(candidateId);

  const [messageText, setMessageText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [logs, setLogs] = useState<string[]>([
    `[SYS_INIT] Initializing Video Assessment Engine (/Luma-Dot-Background)...`,
    `[DOSSIER_VERIFIED] Candidate '${candidateId}' telemetry parsed.`,
    `[AGENT_SPAWN] Spawning AI Interviewer Subagent (ID: agent-qa-9)...`,
    `[CURRICULUM_LOAD] Loading Capstone Mission: 'Model Context Protocol & Multi-Agent Swarms'.`,
    `[PROMPT] "Candidate ${candidate?.name || candidateId}, demonstrate how your MCP server architecture handles tool timeouts under load."`,
  ]);

  // Silent session initialization on component mount
  useEffect(() => {
    if (!candidate) {
      setIsInitializing(false);
      return;
    }

    const initSession = async () => {
      try {
        const res = await fetch('/api/interview', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            sessionId: candidateId,
            candidate: {
              member: {
                id: candidate.id,
                name: candidate.name,
                jobRole: candidate.jobRole,
                yearsExperience: candidate.yearsExperience,
                education: candidate.education,
                status: candidate.status,
              },
              missions: candidate.missions,
              signals: candidate.signals,
            },
          }),
        });

        if (res.ok) {
          const data = await res.json();
          setLogs((prev) => [
            ...prev,
            `[SESSION_INIT] Backend session '${candidateId}' created in InMemorySessionRepository.`,
          ]);
          if (data.reply) {
            setLogs((prev) => [...prev, `[AGENT_REPLY] "${data.reply}"`]);
          }
        }
      } catch (err: any) {
        console.warn('Backend session init warning:', err);
      } finally {
        setIsInitializing(false);
      }
    };

    initSession();
  }, [candidateId, candidate]);

  if (!candidate) {
    return (
      <main className="min-h-screen p-8 flex flex-col items-center justify-center relative z-10 font-bitcount">
        <div className="glass-panel p-8 text-center max-w-md border border-[#C13383]/30">
          <AlertCircle className="w-12 h-12 text-[#E05454] mx-auto mb-4" />
          <h1 className="text-xl font-normal text-white font-bitcount">Candidate Not Found</h1>
          <p className="text-xs text-slate-300 mt-2 mb-6 font-bitcount">
            No candidate dossier found with ID: {candidateId}
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

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = messageText.trim();
    if (!trimmed || isLoading || isInitializing) return;

    // 1. Immediately append user message to terminal log
    setLogs((prev) => [...prev, `[USER_MSG] "${trimmed}"`]);
    setMessageText('');
    setIsLoading(true);

    try {
      // 2. Send POST request to /api/interview proxy
      const res = await fetch('/api/interview', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sessionId: candidateId,
          message: trimmed,
        }),
      });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status} - ${res.statusText}`);
      }

      const data = await res.json();

      // 3. Append reply from FastAPI backend into stream log
      if (data.reply) {
        setLogs((prev) => [...prev, `[AGENT_REPLY] "${data.reply}"`]);
      }

      if (data.feedback && data.feedback.summary) {
        setLogs((prev) => [
          ...prev,
          `[FEEDBACK_SUMMARY] ${data.feedback.summary}`,
        ]);
      }
    } catch (err: any) {
      // 4. Handle HTTP or network errors cleanly
      setLogs((prev) => [
        ...prev,
        `[SYS_ERROR] Request failed: ${err?.message || 'Unable to connect to backend server at /api/interview'}`,
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-4 sm:p-8 max-w-7xl mx-auto relative z-10 font-bitcount">
      {/* Navigation Header */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={() => router.push('/')}
          type="button"
          className="glass-secondary-btn px-4 py-2.5 flex items-center gap-2 text-xs font-bitcount font-normal text-white cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4 text-[#E05454]" />
          Back to Dossiers
        </button>

        <div className="glass-badge px-4 py-1.5 flex items-center gap-3 border border-[#E05454]/40 bg-[#E05454]/15">
          <span className="w-2.5 h-2.5 rounded-full bg-[#E05454] animate-ping" />
          <span className="font-bitcount text-xs font-normal text-white">
            SIMULATION ROOM // {candidate.id}
          </span>
        </div>
      </div>

      {/* Main Glass Terminal Frame */}
      <div className="glass-panel p-6 sm:p-8 mb-6 border border-[#C13383]/35 relative overflow-hidden">
        {/* Ambient Glows */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-[#E05454]/15 rounded-full blur-3xl pointer-events-none" />

        {/* Candidate Profile Bar */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6 pb-6 border-b border-white/15 relative z-10">
          <div className="flex items-center gap-4">
            <div
              className={`w-14 h-14 rounded-2xl ${candidate.avatar} flex items-center justify-center font-bold text-white text-xl shadow-lg border border-white/40 shrink-0`}
            >
              {candidate.name
                .split(' ')
                .map((n) => n[0])
                .join('')}
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-light font-bitcount text-white text-glow-coral">
                  {candidate.name}
                </h1>
                <span className="text-xs font-bitcount font-normal px-2.5 py-0.5 rounded-full bg-[#E05454]/20 text-[#E05454] border border-[#E05454]/30">
                  {candidate.id}
                </span>
              </div>
              <p className="text-xs font-normal text-[#C13383] mt-1 flex items-center gap-2 font-bitcount">
                <Briefcase className="w-3.5 h-3.5" />
                {candidate.jobRole} • {candidate.yearsExperience} Yrs Exp • {candidate.education}
              </p>
            </div>
          </div>

          <div className="glass-well px-5 py-2.5 rounded-2xl border border-[#E05454]/40 bg-[#E05454]/15 flex items-center gap-3 self-stretch md:self-auto justify-center">
            <Award className="w-6 h-6 text-[#E05454] shrink-0" />
            <div>
              <div className="text-[10px] font-bitcount uppercase text-slate-300">
                RATING
              </div>
              <div className="text-xl font-bitcount font-normal text-white">
                {candidate.overallScore} / 100
              </div>
            </div>
          </div>
        </div>

        {/* Terminal Screen & Controller */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10">
          {/* Terminal Output & Interactive Chat Input */}
          <div className="lg:col-span-2 flex flex-col justify-between">
            <div className="flex items-center justify-between font-bitcount text-xs text-slate-200 mb-2">
              <span className="flex items-center gap-2 font-normal">
                <Terminal className="w-4 h-4 text-[#E05454]" />
                REAL-TIME AGENT INTERVIEW STREAM
              </span>
              <span className="text-emerald-400 flex items-center gap-1.5 font-normal">
                <Activity className="w-3.5 h-3.5 animate-pulse" />
                STREAMING
              </span>
            </div>

            {/* Stream Log Terminal Box */}
            <div className="glass-well rounded-2xl p-4 font-bitcount text-xs text-slate-200 h-80 overflow-y-auto space-y-2 border border-white/15 shadow-inner">
              {logs.map((log, idx) => (
                <div
                  key={idx}
                  className={`leading-relaxed ${
                    log.includes('[SYS_ERROR]')
                      ? 'text-rose-400 font-normal bg-rose-500/15 p-2 rounded-lg border border-rose-500/30'
                      : log.includes('[SESSION_INIT]')
                      ? 'text-purple-300 font-normal bg-purple-500/15 p-2 rounded-lg border border-purple-500/30'
                      : log.includes('[SYS')
                      ? 'text-slate-400'
                      : log.includes('[PROMPT]')
                      ? 'text-[#C13383] font-normal bg-[#C13383]/15 p-2 rounded-lg border border-[#C13383]/30'
                      : log.includes('[USER_MSG]')
                      ? 'text-emerald-300 font-normal bg-emerald-500/15 p-2 rounded-lg border border-emerald-500/30'
                      : log.includes('[AGENT_REPLY]')
                      ? 'text-sky-300 font-normal bg-sky-500/15 p-2 rounded-lg border border-sky-500/30'
                      : log.includes('[BENCHMARK]')
                      ? 'text-emerald-300'
                      : 'text-slate-200'
                  }`}
                >
                  {log}
                </div>
              ))}
            </div>

            {/* Functional Chat Input Form Anchored to Bottom */}
            <form onSubmit={handleSendMessage} className="flex items-center gap-2.5 mt-4">
              <input
                type="text"
                disabled={isLoading || isInitializing}
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
                placeholder={
                  isInitializing
                    ? 'Initializing backend session...'
                    : isLoading
                    ? 'Awaiting backend agent response...'
                    : 'Type a message or response for the candidate/agent...'
                }
                className="flex-1 bg-white/5 border border-white/15 text-white placeholder-white/40 px-4 py-2.5 rounded-xl text-xs font-bitcount focus:outline-none focus:ring-1 focus:ring-[#E05454]/60 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              />
              <button
                type="submit"
                disabled={isLoading || isInitializing || !messageText.trim()}
                className="glass-action-btn px-5 py-2.5 rounded-xl text-xs font-bitcount flex items-center gap-2 text-white cursor-pointer shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading || isInitializing ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <Send className="w-3.5 h-3.5" />
                )}
                {isInitializing ? 'Init...' : isLoading ? 'Sending...' : 'Send'}
              </button>
            </form>
          </div>

          {/* Side Evaluation Metrics Panel */}
          <div className="space-y-4 font-bitcount">
            <div className="glass-well rounded-2xl p-4 border border-white/15">
              <h3 className="font-bitcount text-xs font-normal text-slate-200 uppercase mb-3 flex items-center gap-2">
                <Cpu className="w-4 h-4 text-[#E05454]" />
                Active Evaluation Module
              </h3>
              <div className="bg-white/10 p-3.5 rounded-xl border border-white/15 space-y-2">
                <div className="font-normal text-xs text-white">
                  Model Context Protocol (MCP) & Agents
                </div>
                <p className="text-[11px] text-slate-300 leading-relaxed font-bitcount">
                  Evaluating tool schema design, function execution safety, and error handling.
                </p>
                <div className="pt-2 flex items-center justify-between text-[11px] font-bitcount border-t border-white/15">
                  <span className="text-slate-300">Status:</span>
                  <span className="text-emerald-400 font-normal flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> EVALUATING
                  </span>
                </div>
              </div>
            </div>

            {/* Audio Synthesis Hardware Box */}
            <div className="glass-well rounded-2xl p-4 border border-white/15">
              <h3 className="font-bitcount text-xs font-normal text-slate-200 uppercase mb-3 flex items-center gap-2">
                <Mic className="w-4 h-4 text-[#E05454]" />
                Neural Audio Synthesizer
              </h3>
              <div className="flex items-center justify-between text-xs font-bitcount text-slate-200 bg-white/10 p-3 rounded-xl border border-white/15">
                <div className="flex items-center gap-2">
                  <Volume2 className="w-4 h-4 text-emerald-400 animate-pulse" />
                  <span>Real-time Voice Engine</span>
                </div>
                <span className="text-[10px] text-emerald-300 font-normal bg-emerald-500/20 px-2 py-0.5 rounded-full border border-emerald-500/30">
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
