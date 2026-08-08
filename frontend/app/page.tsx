"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { MissionCard } from "@/components/assessment/MissionCard";
import { WorldStateViewer } from "@/components/assessment/WorldStateViewer";
import { sendInterviewTurn, ApiClientError } from "@/lib/api/client";
import { InterviewResponse, MissionData, ProgressData, WorldStateData } from "@/lib/types/interview";
import { Play, Send, CheckCircle2, AlertCircle, RefreshCw } from "lucide-react";

function difficultyToLevel(label?: string | null): number {
  const map: Record<string, number> = { basic: 1, intermediate: 2, advanced: 3, expert: 4 };
  return map[(label || "intermediate").toLowerCase()] || 2;
}

function metricsFromWorld(world?: WorldStateData | null): Record<string, string> {
  if (!world?.system_state) return {};
  const metrics: Record<string, string> = {};
  const state = world.system_state;
  if (state.latency_ms != null) metrics["Latency"] = `${state.latency_ms}ms`;
  if (state.memory_usage_pct != null) metrics["Memory"] = `${state.memory_usage_pct}%`;
  if (state.cache_hit_pct != null) metrics["Cache Hit"] = `${state.cache_hit_pct}%`;
  if (state.recall_score != null) metrics["Recall"] = String(state.recall_score);
  if (state.error_rate_pct != null) metrics["Error Rate"] = `${state.error_rate_pct}%`;
  return metrics;
}

export default function AssessmentPage() {
  const [sessionId, setSessionId] = useState(`session-${Date.now()}`);
  const [candidateName, setCandidateName] = useState("Emily Chen");
  const [jobRole, setJobRole] = useState("AI Engineer");
  const [yearsExp, setYearsExp] = useState(6);

  const [activeSession, setActiveSession] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [message, setMessage] = useState("");
  const [turns, setTurns] = useState<{ sender: "interviewer" | "candidate"; text: string }[]>([]);
  const [finalReport, setFinalReport] = useState<InterviewResponse["feedback"] | null>(null);
  const [mission, setMission] = useState<MissionData | null>(null);
  const [world, setWorld] = useState<WorldStateData | null>(null);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [mode, setMode] = useState<string | null>(null);

  const applyResponse = (res: InterviewResponse) => {
    setMission(res.mission || null);
    setWorld(res.world_state || null);
    setProgress(res.progress || null);
    setMode(res.mode || null);
    if (res.done && res.feedback) {
      setFinalReport(res.feedback);
    }
  };

  const handleStart = async () => {
    setLoading(true);
    setError(null);
    setFinalReport(null);
    try {
      const res = await sendInterviewTurn({
        sessionId,
        candidate: {
          member: {
            id: `CAND-${Math.floor(Math.random() * 900 + 100)}`,
            name: candidateName,
            jobRole,
            yearsExperience: Number(yearsExp),
            education: "MS Artificial Intelligence",
            status: "ACTIVE",
          },
          missions: [],
          signals: { commitDays: 31, missionsCompleted: 15, missionsFirstTry: 14 },
        },
      });

      setActiveSession(true);
      setTurns([{ sender: "interviewer", text: res.reply }]);
      applyResponse(res);
    } catch (err) {
      if (err instanceof ApiClientError) {
        setError(`${err.message} (${err.code})`);
      } else {
        setError("Failed to initialize assessment session.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSendTurn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || loading) return;

    const userMsg = message.trim();
    setMessage("");
    setTurns((prev) => [...prev, { sender: "candidate", text: userMsg }]);
    setLoading(true);
    setError(null);

    try {
      const res = await sendInterviewTurn({
        sessionId,
        message: userMsg,
      });

      setTurns((prev) => [...prev, { sender: "interviewer", text: res.reply }]);
      applyResponse(res);
    } catch (err) {
      if (err instanceof ApiClientError) {
        setError(`${err.message} (${err.code})`);
      } else {
        setError("Failed to process conversation turn.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    setError(null);
    setActiveSession(false);
    setTurns([]);
    setFinalReport(null);
    setMission(null);
    setWorld(null);
    setProgress(null);
    setMode(null);
    setSessionId(`session-${Date.now()}`);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 glass-panel rounded-2xl border-sky-500/20 bg-gradient-to-r from-slate-900 via-slate-900 to-sky-950/40">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="info">Adaptive Mission Arc</Badge>
            <span className="text-xs font-mono text-slate-400">Session ID: {sessionId}</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100">AI Engineering Mission Control</h1>
          <p className="text-sm text-slate-400 mt-1">
            Live technical assessment evaluating architecture, retrieval debugging, and systems judgment.
          </p>
        </div>

        {!activeSession ? (
          <Button onClick={handleStart} disabled={loading} size="lg">
            {loading ? <RefreshCw className="w-5 h-5 animate-spin mr-2" /> : <Play className="w-5 h-5 mr-2" />}
            Initialize Session
          </Button>
        ) : (
          <div className="flex items-center gap-2">
            <Badge variant="success" className="px-3 py-1 text-sm">
              {finalReport ? "Session Complete" : mode ? `Active · ${mode}` : "Session Active"}
            </Badge>
            <Button variant="ghost" onClick={handleRetry} size="sm">
              Reset
            </Button>
          </div>
        )}
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-950/60 border border-rose-500/40 text-rose-200 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
          <span className="flex-1">{error}</span>
          <Button variant="ghost" size="sm" onClick={handleRetry}>
            Retry
          </Button>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-6 lg:col-span-1">
          {!activeSession ? (
            <Card>
              <CardHeader title="Candidate Calibration" subtitle="Role bar & experience inputs" />
              <div className="space-y-4 text-sm">
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Session Key</label>
                  <input
                    type="text"
                    value={sessionId}
                    onChange={(e) => setSessionId(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-200 focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Candidate Name</label>
                  <input
                    type="text"
                    value={candidateName}
                    onChange={(e) => setCandidateName(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-200 focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Target Job Role</label>
                  <input
                    type="text"
                    value={jobRole}
                    onChange={(e) => setJobRole(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-200 focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Years of Experience</label>
                  <input
                    type="number"
                    value={yearsExp}
                    onChange={(e) => setYearsExp(Number(e.target.value))}
                    className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-200 focus:outline-none focus:border-sky-500"
                  />
                </div>
              </div>
            </Card>
          ) : (
            <>
              {progress && (
                <Card>
                  <CardHeader title="Interview Progress" subtitle="Coverage against minimum requirements" />
                  <div className="text-xs text-slate-300 space-y-1 font-mono">
                    <p>
                      Questions: {progress.question_number} / {progress.minimum_questions}
                    </p>
                    <p>
                      Curriculum days: {progress.curriculum_days_covered} / {progress.minimum_curriculum_days}
                    </p>
                    <p>Covered: {progress.covered_curriculum_days.join(", ") || "—"}</p>
                  </div>
                </Card>
              )}
              {mission ? (
                <MissionCard
                  title={mission.title}
                  scenario={mission.scenario}
                  difficulty={difficultyToLevel(mission.difficulty)}
                  competency={mission.competency}
                />
              ) : (
                <Card>
                  <CardHeader title="Awaiting Mission" subtitle="Mission details appear after the interviewer responds." />
                </Card>
              )}
              {world ? (
                <WorldStateViewer
                  version={world.version}
                  summary={world.visible_summary}
                  metrics={metricsFromWorld(world)}
                />
              ) : null}
            </>
          )}
        </div>

        <div className="lg:col-span-2 space-y-6">
          <Card className="min-h-[480px] flex flex-col justify-between">
            <CardHeader
              title="Interactive Engineering Console"
              subtitle={
                activeSession
                  ? "Respond with debugging hypotheses, architecture choices, or commands."
                  : "Session pending initialization."
              }
            />

            <div className="flex-1 space-y-4 overflow-y-auto max-h-[380px] pr-2 my-4">
              {turns.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-slate-500 py-12">
                  <CheckCircle2 className="w-12 h-12 mb-2 stroke-1 text-slate-600" />
                  <p className="text-sm">Click &quot;Initialize Session&quot; to launch candidate assessment.</p>
                </div>
              ) : (
                turns.map((t, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-xl text-sm leading-relaxed ${
                      t.sender === "interviewer"
                        ? "bg-slate-900 border border-slate-800 text-slate-200"
                        : "bg-sky-950/60 border border-sky-500/30 text-sky-100 ml-6"
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-2">
                      <span className="font-semibold text-sky-400">
                        {t.sender === "interviewer" ? "CHIMERA INTERVIEWER" : "CANDIDATE RESPONSE"}
                      </span>
                      <span>Turn #{idx + 1}</span>
                    </div>
                    <p className="whitespace-pre-wrap">{t.text}</p>
                  </div>
                ))
              )}
            </div>

            {activeSession && !finalReport && (
              <form onSubmit={handleSendTurn} className="flex gap-3 pt-4 border-t border-slate-800">
                <input
                  type="text"
                  placeholder="Type your engineering analysis or answer..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  disabled={loading}
                  className="flex-1 px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500 text-sm"
                />
                <Button type="submit" disabled={loading || !message.trim()}>
                  {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                </Button>
              </form>
            )}
          </Card>

          {finalReport && (
            <Card className="border-emerald-500/30 bg-emerald-950/20">
              <CardHeader title="Assessment Summary & Feedback" subtitle="Evidence-based report" />
              <div className="space-y-3 text-sm">
                <p className="text-slate-200">{finalReport.summary}</p>
                {finalReport.hiring_assessment && (
                  <p className="text-slate-300 text-xs">{finalReport.hiring_assessment}</p>
                )}
                <div>
                  <h4 className="font-semibold text-emerald-400 text-xs uppercase tracking-wider">Strengths</h4>
                  <ul className="list-disc list-inside text-slate-300 text-xs mt-1">
                    {finalReport.strengths.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-amber-400 text-xs uppercase tracking-wider">Gaps</h4>
                  <ul className="list-disc list-inside text-slate-300 text-xs mt-1">
                    {finalReport.gaps.map((g, i) => (
                      <li key={i}>{g}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-sky-400 text-xs uppercase tracking-wider">Next Steps</h4>
                  <ul className="list-disc list-inside text-slate-300 text-xs mt-1">
                    {finalReport.next.map((n, i) => (
                      <li key={i}>{n}</li>
                    ))}
                  </ul>
                </div>
                {finalReport.engineering_dna && Object.keys(finalReport.engineering_dna).length > 0 && (
                  <div>
                    <h4 className="font-semibold text-violet-300 text-xs uppercase tracking-wider">Engineering DNA</h4>
                    <ul className="list-disc list-inside text-slate-300 text-xs mt-1">
                      {Object.entries(finalReport.engineering_dna).map(([k, v]) => (
                        <li key={k}>
                          {k}: {v.toFixed(2)}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
