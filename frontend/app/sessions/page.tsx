"use client";

import React from "react";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Activity, Clock, User, Award } from "lucide-react";

export default function SessionsPage() {
  const mockSessions = [
    {
      id: "session-demo-001",
      candidate: "Emily Chen",
      role: "AI Engineer",
      seniority: "Senior",
      status: "active",
      turns: 3,
      createdAt: "2026-08-08 12:30 UTC",
    },
    {
      id: "session-demo-002",
      candidate: "Marcus Vance",
      role: "ML Platform Engineer",
      seniority: "Staff",
      status: "completed",
      turns: 8,
      createdAt: "2026-08-07 16:15 UTC",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="p-6 glass-panel rounded-2xl border-slate-800">
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Activity className="w-6 h-6 text-sky-400" /> Assessment Sessions
        </h1>
        <p className="text-sm text-slate-400 mt-1">Audit log of ongoing and completed candidate interview sessions.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {mockSessions.map((s) => (
          <Card key={s.id} className="border-slate-800">
            <div className="flex justify-between items-start mb-3">
              <div className="flex items-center gap-2">
                <User className="w-4 h-4 text-sky-400" />
                <span className="font-semibold text-slate-100">{s.candidate}</span>
              </div>
              <Badge variant={s.status === "active" ? "info" : "success"}>
                {s.status.toUpperCase()}
              </Badge>
            </div>

            <CardHeader title={s.role} subtitle={`Seniority: ${s.seniority}`} />

            <div className="flex justify-between items-center text-xs text-slate-400 pt-3 border-t border-slate-800/80">
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-slate-500" /> {s.createdAt}
              </span>
              <span className="flex items-center gap-1 font-mono">
                <Award className="w-3.5 h-3.5 text-amber-400" /> {s.turns} Turns
              </span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
