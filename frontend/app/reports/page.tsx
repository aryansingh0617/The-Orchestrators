"use client";

import React from "react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Shield, FileCheck, AlertCircle } from "lucide-react";

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div className="p-6 glass-panel rounded-2xl border-slate-800">
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Shield className="w-6 h-6 text-emerald-400" /> Candidate Evaluation Reports
        </h1>
        <p className="text-sm text-slate-400 mt-1">Evidence-backed hiring recommendations & candidate feedback.</p>
      </div>

      <Card className="border-slate-800">
        <div className="flex justify-between items-start mb-4">
          <div>
            <span className="text-xs font-mono text-slate-400">Candidate: Emily Chen (Senior AI Engineer)</span>
            <h2 className="text-xl font-bold text-slate-100 mt-0.5">Evaluation & Hiring Recommendation</h2>
          </div>
          <Badge variant="success">Recommendation: Strong Hire (Confidence: 88%)</Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
            <span className="text-xs font-mono text-slate-400">Systems Thinking</span>
            <p className="text-lg font-bold text-sky-400 mt-1">4.5 / 5.0</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
            <span className="text-xs font-mono text-slate-400">Debugging & Diagnosis</span>
            <p className="text-lg font-bold text-emerald-400 mt-1">4.8 / 5.0</p>
          </div>
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
            <span className="text-xs font-mono text-slate-400">Production Engineering</span>
            <p className="text-lg font-bold text-amber-400 mt-1">4.0 / 5.0</p>
          </div>
        </div>

        <div className="space-y-4 text-sm text-slate-300">
          <CardHeader title="Evidence Summary" subtitle="Key observed signals" />
          <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 flex items-start gap-2">
            <FileCheck className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
            <span>Isolated chunk size reduction as root cause of recall drop before touching prompt templates.</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 flex items-start gap-2">
            <FileCheck className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
            <span>Proposed observability metrics (vector cache hit %, tail latency) prior to shipping mitigations.</span>
          </div>

          <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 text-amber-200 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
            <span>Human Review Note: Recommendation is evidence-backed. Human interviewer confirmation recommended prior to offer.</span>
          </div>
        </div>
      </Card>
    </div>
  );
}
