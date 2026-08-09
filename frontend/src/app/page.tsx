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
import { getCandidates, Candidate } from "@/lib/candidates";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export default function GeminiInterviewerChatPage() {
  const [candidates] = useState<Candidate[]>(() => getCandidates());
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(
    () => candidates[0] || null
  );

  const [sessionId] = useState<string>(
    () => `gemini-session-${Math.random().toString(36).substring(2, 9)}`
  );

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "init-1",
      role: "assistant",
      content:
        "Greetings! I am your AI Technical Interviewer powered by Google Gemini.\n\nToday we will assess your grasp of complex AI architectures—specifically RAG pipelines, vector search indexing, and high-availability production mitigations.\n\nTo begin, how would you address a production incident where vector search query recall drops to 0.71 and error rate spikes to 2.4%?",
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

    const newHistory = [...messages, userMsg];
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
          candidate_info: selectedCandidate
            ? {
                id: selectedCandidate.id,
                name: selectedCandidate.name,
                jobRole: selectedCandidate.jobRole,
                education: selectedCandidate.education,
              }
            : null,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      const aiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        role: "assistant",
        content:
          data.reply || "I have recorded your response. What would you analyze next?",
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error("[ChatUI] Error sending message:", err);
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: "assistant",
        content:
          "⚠️ Communication note: Unable to connect to backend server. Retrying backoff mechanism active.",
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
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
        content: `Session reset for candidate ${
          selectedCandidate ? selectedCandidate.name : "Applicant"
        }. Welcome! Let us begin our technical assessment. Please describe your strategy for optimizing vector database query recall and error handling.`,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);
  };

  return (
    <main className="min-h-screen p-3 sm:p-6 lg:p-8 max-w-6xl mx-auto flex flex-col justify-between relative z-10 font-bitcount">
      {/* Top Header Navigation */}
      <header className="glass-panel p-4 sm:p-5 mb-4 flex flex-col sm:flex-row items-center justify-between gap-4 border border-white/20">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-[#E05454] to-[#C13383] p-0.5 flex items-center justify-center shadow-lg shadow-[#E05454]/30">
            <div className="w-full h-full bg-[#130A24] rounded-[14px] flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-[#E05454] animate-pulse" />
            </div>
          </div>
          <div>
            <h1 className="text-lg sm:text-xl font-normal text-white uppercase tracking-wider text-glow-coral">
              PROJECT CHIMERA // GEMINI INTERVIEWER
            </h1>
            <p className="text-xs text-[#D6D6D6] flex items-center gap-2">
              <Zap className="w-3.5 h-3.5 text-amber-400" /> Adaptive Gemini 1.5 Flash Technical Assessment Engine
            </p>
          </div>
        </div>

        {/* Candidate Selector */}
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <select
            value={selectedCandidate?.id || ""}
            onChange={(e) => {
              const cand = candidates.find((c) => c.id === e.target.value) || null;
              setSelectedCandidate(cand);
            }}
            className="glass-well text-xs text-white px-3 py-2 rounded-xl border border-white/20 focus:outline-none focus:border-[#E05454] cursor-pointer w-full sm:w-auto"
          >
            {candidates.map((cand) => (
              <option key={cand.id} value={cand.id} className="bg-[#130A24] text-white">
                {cand.id} - {cand.name} ({cand.jobRole})
              </option>
            ))}
          </select>

          <button
            onClick={handleResetSession}
            type="button"
            title="Reset Interview Session"
            className="glass-secondary-btn p-2 rounded-xl text-[#E05454] hover:text-white"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* Main Chat Conversation Container */}
      <section className="glass-panel p-4 sm:p-6 flex-1 flex flex-col justify-between min-h-[550px] max-h-[70vh] overflow-hidden border border-white/20 relative">
        {/* Scrollable Message History Area */}
        <div className="flex-1 overflow-y-auto pr-2 space-y-4 scrollbar-thin scrollbar-thumb-white/20">
          {messages.map((msg) => {
            const isUser = msg.role === "user";
            return (
              <div
                key={msg.id}
                className={`flex gap-3 max-w-[88%] sm:max-w-[78%] ${
                  isUser ? "ml-auto flex-row-reverse" : "mr-auto"
                }`}
              >
                {/* Avatar Icon */}
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 border shadow-md ${
                    isUser
                      ? "bg-gradient-to-br from-[#E05454] to-[#C13383] border-white/40 text-white"
                      : "bg-[#1E1035] border-[#E05454]/60 text-[#E05454]"
                  }`}
                >
                  {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>

                {/* Message Bubble Content */}
                <div
                  className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                    isUser
                      ? "bg-gradient-to-br from-[#E05454]/90 to-[#C13383]/90 text-white border border-white/30 shadow-lg shadow-[#E05454]/20 rounded-tr-none"
                      : "glass-card text-[#E2E8F0] border border-white/20 shadow-md rounded-tl-none"
                  }`}
                >
                  <div className="flex items-center justify-between gap-3 mb-1.5 opacity-80 text-[10px] uppercase tracking-wider font-mono">
                    <span className="font-semibold">{isUser ? selectedCandidate?.name || "Candidate" : "Gemini Technical Interviewer"}</span>
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
            <div className="flex gap-3 mr-auto max-w-[80%]">
              <div className="w-8 h-8 rounded-full bg-[#1E1035] border border-[#E05454]/60 text-[#E05454] flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 animate-spin" />
              </div>
              <div className="glass-card p-4 rounded-2xl rounded-tl-none border border-white/20 flex items-center gap-3">
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
        <div className="pt-3 pb-2 flex flex-wrap items-center gap-2 border-t border-white/10 mt-3">
          <span className="text-[10px] text-[#D6D6D6] uppercase tracking-wider flex items-center gap-1">
            <Zap className="w-3 h-3 text-[#E05454]" /> Quick Technical Probes:
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
        <form onSubmit={handleSend} className="mt-2 flex items-center gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your technical response or question... (Press Enter to send, Shift+Enter for newline)"
            rows={2}
            className="flex-1 glass-well text-xs sm:text-sm text-white placeholder-slate-400 p-3 rounded-2xl border border-white/20 focus:outline-none focus:border-[#E05454] resize-none"
          />

          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="glass-action-btn h-12 px-5 text-xs font-bold flex items-center gap-2 rounded-2xl disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
          >
            <span>Send</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </form>
      </section>

      {/* Footer Branding */}
      <footer className="mt-4 text-center text-[11px] text-[#D6D6D6] opacity-80 flex items-center justify-center gap-2">
        <Sparkles className="w-3.5 h-3.5 text-[#C13383]" />
        PROJECT CHIMERA ASSESSMENT OS // FASTAPI + GOOGLE GEMINI 1.5 FLASH
      </footer>
    </main>
  );
}
