import React from "react";
import { Card, CardHeader } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { Target, AlertTriangle } from "lucide-react";

interface MissionCardProps {
  title: string;
  scenario: string;
  difficulty: number;
  competency: string;
}

export function MissionCard({ title, scenario, difficulty, competency }: MissionCardProps) {
  return (
    <Card className="border-sky-500/30 bg-slate-900/90 glow-accent">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Target className="w-5 h-5 text-sky-400" />
          <Badge variant="info">Active Mission</Badge>
        </div>
        <Badge variant="warning">Difficulty: L{difficulty}</Badge>
      </div>

      <CardHeader title={title} subtitle={`Target Competency: ${competency}`} />

      <div className="p-4 rounded-lg bg-slate-950/80 border border-slate-800 text-slate-300 text-sm leading-relaxed space-y-2">
        <div className="flex items-start gap-2 text-slate-400 font-mono text-xs uppercase tracking-wider mb-1">
          <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0" />
          <span>Incident Context & Mission Brief</span>
        </div>
        <p>{scenario}</p>
      </div>
    </Card>
  );
}
