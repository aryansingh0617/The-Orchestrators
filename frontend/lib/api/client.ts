import { InterviewRequest, InterviewResponse, ApiErrorResponse } from "../types/interview";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export class ApiClientError extends Error {
  code: string;
  details?: Record<string, unknown>;
  traceId?: string;

  constructor(message: string, code: string = "client_error", details?: Record<string, unknown>, traceId?: string) {
    super(message);
    this.name = "ApiClientError";
    this.code = code;
    this.details = details;
    this.traceId = traceId;
  }
}

export async function sendInterviewTurn(payload: InterviewRequest): Promise<InterviewResponse> {
  const url = `${API_BASE_URL}/api/interview`;
  
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      let errData: ApiErrorResponse | null = null;
      try {
        errData = await res.json();
      } catch {
        // Fallback if response isn't JSON
      }

      if (errData?.error) {
        throw new ApiClientError(
          errData.error.message,
          errData.error.code,
          errData.error.details,
          errData.error.trace_id
        );
      }
      throw new ApiClientError(`API request failed with status ${res.status}`);
    }

    return await res.json();
  } catch (err) {
    if (err instanceof ApiClientError) {
      throw err;
    }
    throw new ApiClientError((err as Error).message || "Network request failed");
  }
}

export async function checkHealth(): Promise<{ status: string; service: string; version: string }> {
  const url = `${API_BASE_URL}/health`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new ApiClientError("Health check failed");
  }
  return res.json();
}
