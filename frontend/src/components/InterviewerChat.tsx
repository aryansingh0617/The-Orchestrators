"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  Sparkles,
  Send,
  User,
  Bot,
  RefreshCw,
  MessageSquare,
  ShieldAlert,
  Zap,
  Award,
  BookOpen,
} from "lucide-react";
import { Candidate } from "@/lib/candidates";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  isError?: boolean;
}

interface InterviewerChatProps {
  candidate?: Candidate | null;
  sessionKey?: string;
}

export function InterviewerChat({ candidate, sessionKey }: InterviewerChatProps) {
  const candidateName = candidate?.name || "Candidate";
  const candidateId = candidate?.id || "CAND-001";
  const candidateRole = candidate?.jobRole || "AI Engineer";

  const [sessionId] = useState<string>(
    () => sessionKey || `gemini-session-${candidateId}-${Math.random().toString(36).substring(2, 7)}`
  );

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "init-1",
      role: "assistant",
      content: `Greetings! I am your AI Technical Interviewer powered by Google Gemini.\n\nToday we are conducting a technical evaluation for candidate ${candidateName} (${candidateId} • ${candidateRole}).\n\nTo begin, how would you address a production incident where vector search query recall drops to 0.71 and error rate spikes to 2.4%?`,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);

  const [input, setInput] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const userText = input.trim();
    if (!userText || isLoading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: userText,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    const newHistory = [...messages.filter((m) => !m.isError), userMsg];
    setMessages(newHistory);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("/api/interview/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId: sessionId,
          message: userText,
          chat_history: newHistory.map((m) => ({
            role: m.role,
            content: m.content,
          })),
          candidate_info: candidate
            ? {
                id: candidate.id,
                name: candidate.name,
                jobRole: candidate.jobRole,
                education: candidate.education,
              }
            : {
                id: candidateId,
                name: candidateName,
                jobRole: candidateRole,
              },
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || data.message || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      const aiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        role: "assistant",
        content: data.reply,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err: any) {
      console.error("[InterviewerChat] Error sending message to Gemini API:", err);
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: "assistant",
        content: `🚨 Gemini API Execution Error:\n${err?.message || "Failed to communicate with live Gemini backend service."}`,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleQuickPrompt = (promptText: string) => {
    setInput(promptText);
  };

  const handleResetSession = () => {
    setMessages([
      {
        id: `init-${Date.now()}`,
        role: "assistant",
        content: `Session reset for ${candidateName} (${candidateId}). Welcome! Let us begin our technical assessment. Please describe your strategy for optimizing vector database query recall and error handling.`,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);
  };

  return (
    <div className="glass-panel p-4 sm:p-6 flex flex-col justify-between border border-[#C13383]/35 relative overflow-hidden">
      {/* Top Session Header Bar */}
      <div className="flex items-center justify-between pb-4 mb-4 border-b border-white/15">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-[#E05454] to-[#C13383] p-0.5 flex items-center justify-center shadow-md">
            <div className="w-full h-full bg-[#130A24] rounded-[10px] flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-[#E05454] animate-pulse" />
            </div>
          </div>
          <div>
            <h3 className="text-sm font-normal text-white uppercase tracking-wider font-bitcount text-glow-coral flex items-center gap-2">
              GEMINI AI INTERVIEWER // {candidateId}
            </h3>
            <p className="text-[11px] text-[#D6D6D6] font-bitcount">
              Evaluating candidate: <span className="text-white font-semibold">{candidateName}</span> ({candidateRole})
            </p>
          </div>
        </div>

        <button
          onClick={handleResetSession}
          type="button"
          title="Reset Interview Session"
          className="glass-secondary-btn p-2 rounded-xl text-[#E05454] hover:text-white transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Scrollable Message History Area */}
      <div className="h-80 sm:h-96 overflow-y-auto pr-2 space-y-4 font-bitcount scrollbar-thin scrollbar-thumb-white/20">
        {messages.map((msg) => {
          const isUser = msg.role === "user";
          const isError = msg.isError;
          return (
            <div
              key={msg.id}
              className={`flex gap-3 max-w-[88%] sm:max-w-[82%] ${
                isUser ? "ml-auto flex-row-reverse" : "mr-auto"
              }`}
            >
              {/* Avatar Icon */}
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 border shadow-md ${
                  isError
                    ? "bg-rose-950 border-rose-500 text-rose-400"
                    : isUser
                    ? "bg-gradient-to-br from-[#E05454] to-[#C13383] border-white/40 text-white"
                    : "bg-[#1E1035] border-[#E05454]/60 text-[#E05454]"
                }`}
              >
                {isUser ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
              </div>

              {/* Message Bubble Content */}
              <div
                className={`p-3.5 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                  isError
                    ? "bg-rose-950/80 text-rose-200 border border-rose-500/50 shadow-lg shadow-rose-950/50 rounded-tl-none font-mono"
                    : isUser
                    ? "bg-gradient-to-br from-[#E05454]/90 to-[#C13383]/90 text-white border border-white/30 shadow-lg shadow-[#E05454]/20 rounded-tr-none"
                    : "glass-card text-[#E2E8F0] border border-white/20 shadow-md rounded-tl-none"
                }`}
              >
                <div className="flex items-center justify-between gap-3 mb-1 opacity-80 text-[10px] uppercase tracking-wider font-mono">
                  <span className="font-semibold">
                    {isError ? "System Exception" : isUser ? candidateName : "Gemini Technical Interviewer"}
                  </span>
                  <span>{msg.timestamp}</span>
                </div>

                <div className="whitespace-pre-wrap font-sans leading-relaxed text-slate-100">
                  {msg.content}
                </div>
              </div>
            </div>
          );
        })}

        {/* Visible Loading State */}
        {isLoading && (
          <div className="flex gap-3 mr-auto max-w-[80%] font-bitcount">
            <div className="w-7 h-7 rounded-full bg-[#1E1035] border border-[#E05454]/60 text-[#E05454] flex items-center justify-center shrink-0">
              <Bot className="w-3.5 h-3.5 animate-spin" />
            </div>
            <div className="glass-card p-3 rounded-2xl rounded-tl-none border border-white/20 flex items-center gap-3">
              <span className="text-xs text-[#E05454] font-medium tracking-wide">
                Interviewer is typing...
              </span>
              <div className="flex items-center gap-1">
                <div className="w-1.5 h-1.5 bg-[#E05454] rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="w-1.5 h-1.5 bg-[#C13383] rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-1.5 h-1.5 bg-amber-400 rounded-full animate-bounce"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Suggestion Prompt Chips */}
      <div className="pt-3 pb-2 flex flex-wrap items-center gap-2 border-t border-white/10 mt-3 font-bitcount">
        <span className="text-[10px] text-[#D6D6D6] uppercase tracking-wider flex items-center gap-1">
          <Zap className="w-3 h-3 text-[#E05454]" /> Technical Probes:
        </span>
        <button
          onClick={() =>
            handleQuickPrompt(
              "We applied exponential backoff retries and fallback handlers to cut error rate below 0.5%."
            )
          }
          type="button"
          className="glass-secondary-btn text-[11px] px-3 py-1 rounded-full text-slate-200 hover:text-white"
        >
          <ShieldAlert className="w-3 h-3 text-red-400 inline mr-1" />
          Exponential Backoff
        </button>

        <button
          onClick={() =>
            handleQuickPrompt(
              "We upgraded the retrieval pipeline to Hybrid Search combining BM25 keyword matching with dense embeddings."
            )
          }
          type="button"
          className="glass-secondary-btn text-[11px] px-3 py-1 rounded-full text-slate-200 hover:text-white"
        >
          <BookOpen className="w-3 h-3 text-amber-400 inline mr-1" />
          BM25 Hybrid Search
        </button>

        <button
          onClick={() =>
            handleQuickPrompt(
              "We adjusted the semantic cache similarity threshold to capture functionally identical queries."
            )
          }
          type="button"
          className="glass-secondary-btn text-[11px] px-3 py-1 rounded-full text-slate-200 hover:text-white"
        >
          <MessageSquare className="w-3 h-3 text-pink-400 inline mr-1" />
          Cache Threshold
        </button>

        <button
          onClick={() =>
            handleQuickPrompt(
              "Please evaluate my responses across this session and provide constructive interview feedback."
            )
          }
          type="button"
          className="glass-secondary-btn text-[11px] px-3 py-1 rounded-full text-slate-200 hover:text-white"
        >
          <Award className="w-3 h-3 text-emerald-400 inline mr-1" />
          Conclude & Feedback
        </button>
      </div>

      {/* Input Form at Bottom */}
      <form onSubmit={handleSend} className="mt-2 flex items-center gap-2 font-bitcount">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your technical response or question... (Press Enter to send)"
          rows={2}
          className="flex-1 glass-well text-xs text-white placeholder-slate-400 p-3 rounded-2xl border border-white/20 focus:outline-none focus:border-[#E05454] resize-none"
        />

        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="glass-action-btn h-11 px-4 text-xs font-bold flex items-center gap-2 rounded-2xl disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
        >
          <span>Send</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
}
