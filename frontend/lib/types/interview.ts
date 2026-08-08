export interface CandidateMember {
  id: string;
  name?: string;
  jobRole?: string;
  yearsExperience?: number;
  education?: string;
  status?: string;
}

export interface CandidateMission {
  day: number;
  title: string;
  passed?: boolean;
  skipped?: boolean;
  attempts?: number;
}

export interface CandidateSignals {
  commitDays?: number;
  missionsCompleted?: number;
  missionsFirstTry?: number;
}

export interface CandidateData {
  member: CandidateMember;
  missions?: CandidateMission[];
  signals?: CandidateSignals | Record<string, unknown>;
}

export interface FeedbackData {
  summary: string;
  strengths: string[];
  gaps: string[];
  next: string[];
  engineering_dna?: Record<string, number>;
  hiring_assessment?: string | null;
}

export interface MissionData {
  title: string;
  scenario: string;
  context?: string;
  constraints?: string[];
  objective?: string;
  competency: string;
  curriculum_day: number;
  difficulty: string;
  mission_type?: string;
}

export interface WorldStateData {
  visible_summary: string;
  system_state: Record<string, unknown>;
  version: number;
  candidate_decisions?: string[];
}

export interface ProgressData {
  question_number: number;
  curriculum_days_covered: number;
  covered_curriculum_days: number[];
  minimum_questions: number;
  minimum_curriculum_days: number;
}

export interface EvaluationSummaryData {
  outcome: string;
  overall_score?: number | null;
  rationale?: string;
}

export interface InterviewRequest {
  sessionId: string;
  candidate?: CandidateData;
  message?: string;
}

export interface InterviewResponse {
  reply: string;
  done: boolean;
  feedback?: FeedbackData | null;
  session_id?: string | null;
  question_number?: number | null;
  curriculum_day?: number | null;
  competency?: string | null;
  mission?: MissionData | null;
  world_state?: WorldStateData | null;
  progress?: ProgressData | null;
  evaluation_summary?: EvaluationSummaryData | null;
  mode?: string | null;
}

export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    trace_id?: string;
  };
}
