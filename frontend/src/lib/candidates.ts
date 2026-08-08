import assessmentData from '../../data/candidates.json';

export interface CandidateMember {
  id: string;
  name: string;
  jobRole: string;
  yearsExperience: number;
  education: string;
  status: string;
}

export interface CandidateMission {
  day: number;
  title: string;
  passed?: boolean;
  skipped?: boolean;
  attempts?: number;
}

export interface CandidateSignals {
  commitDays: number;
  missionsCompleted: number;
  missionsFirstTry: number;
}

export interface Candidate {
  member: CandidateMember;
  missions: CandidateMission[];
  signals: CandidateSignals;
  // Computed fields
  id: string;
  name: string;
  jobRole: string;
  yearsExperience: number;
  education: string;
  status: string;
  passedMissions: CandidateMission[];
  skippedMissions: CandidateMission[];
  passRate: number;
  firstTryRate: number;
  overallScore: number;
  avatar: string;
}

export interface Module {
  n: number;
  title: string;
  days: [number, number];
}

export interface DayDefinition {
  day: number;
  title: string;
  type: string;
  tools: string[];
  objectives: string[];
}

const AVATAR_GRADIENTS = [
  'bg-gradient-to-br from-cyan-400 to-blue-600',
  'bg-gradient-to-br from-emerald-400 to-teal-600',
  'bg-gradient-to-br from-purple-400 to-indigo-600',
  'bg-gradient-to-br from-amber-400 to-rose-600',
  'bg-gradient-to-br from-pink-400 to-purple-600',
  'bg-gradient-to-br from-sky-400 to-indigo-600',
];

export function getCohortInfo() {
  return {
    cohort: assessmentData.cohort,
    modules: assessmentData.modules as Module[],
    days: assessmentData.days as DayDefinition[],
  };
}

export function getCandidates(): Candidate[] {
  const rawCandidates = assessmentData.candidates;

  return rawCandidates.map((c, idx) => {
    const passedMissions = c.missions.filter((m) => m.passed);
    const skippedMissions = c.missions.filter((m) => m.skipped);

    const completed = c.signals.missionsCompleted;
    const firstTry = c.signals.missionsFirstTry;
    const commitDays = c.signals.commitDays;

    // Calculate score out of 100 based on completion, first try accuracy, and commit activity
    const completionWeight = (completed / 31) * 50; // up to 50 pts
    const accuracyWeight = (firstTry / (completed || 1)) * 30; // up to 30 pts
    const consistencyWeight = (commitDays / 31) * 20; // up to 20 pts
    const overallScore = Math.min(100, Math.round(completionWeight + accuracyWeight + consistencyWeight));

    const passRate = Math.round((completed / 31) * 100);
    const firstTryRate = Math.round((firstTry / (completed || 1)) * 100);

    return {
      ...c,
      id: c.member.id,
      name: c.member.name,
      jobRole: c.member.jobRole,
      yearsExperience: c.member.yearsExperience,
      education: c.member.education,
      status: c.member.status,
      passedMissions,
      skippedMissions,
      passRate,
      firstTryRate,
      overallScore,
      avatar: AVATAR_GRADIENTS[idx % AVATAR_GRADIENTS.length],
    };
  });
}

export function getCandidateById(id: string): Candidate | undefined {
  const candidates = getCandidates();
  return candidates.find((c) => c.id.toLowerCase() === id.toLowerCase());
}
