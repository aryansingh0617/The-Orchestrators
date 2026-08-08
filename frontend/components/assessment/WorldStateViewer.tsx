import React from "react";
import { Card, CardHeader } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { Server } from "lucide-react";

interface WorldStateProps {
  version: number;
  summary: string;
  metrics?: Record<string, string | number>;
}

export function WorldStateViewer({ version, summary, metrics }: WorldStateProps) {
  return (
    <Card className="border-slate-800 bg-slate-900/60">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Server className="w-4 h-4 text-emerald-400" />
          <span className="text-xs font-mono text-slate-400">Simulated World State v{version}</span>
        </div>
        <Badge variant="success">Environment Active</Badge>
      </div>

      <CardHeader title="System Status & Telemetry" />

      <p className="text-sm text-slate-300 mb-4">{summary || "Telemetry normal. Monitoring response actions."}</p>

      {metrics && Object.keys(metrics).length > 0 && (
        <div className="grid grid-cols-2 gap-2 text-xs font-mono">
          {Object.entries(metrics).map(([key, val]) => (
            <div key={key} className="p-2 rounded bg-slate-950/60 border border-slate-800 flex justify-between">
              <span className="text-slate-400">{key}:</span>
              <span className="text-sky-300 font-semibold">{val}</span>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
