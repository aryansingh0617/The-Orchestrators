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
}

export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    trace_id?: string;
  };
}
