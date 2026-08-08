'use client';

import React from 'react';
import { Play, Sparkles } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface TactileButtonProps {
  candidateId: string;
  label?: string;
  size?: 'md' | 'lg' | 'xl';
  onClick?: () => void;
}

export function TactileButton({
  candidateId,
  label = 'Start AI Interview',
  size = 'xl',
  onClick,
}: TactileButtonProps) {
  const router = useRouter();

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onClick) onClick();
    router.push(`/interview/${candidateId}`);
  };

  const sizeClasses = {
    md: 'py-2.5 px-6 text-sm',
    lg: 'py-3.5 px-8 text-base',
    xl: 'py-4 sm:py-5 px-8 sm:px-12 text-base sm:text-xl',
  };

  return (
    <button
      onClick={handleClick}
      type="button"
      className={`glass-action-btn ${sizeClasses[size]} group relative flex items-center justify-center gap-3 w-full max-w-md mx-auto`}
    >
      {/* Ambient Pulsing Glow Layer */}
      <span className="absolute inset-0 bg-gradient-to-r from-[#E0563F]/40 via-[#D174D2]/40 to-[#3F567F]/40 opacity-70 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none blur-md" />

      {/* Illuminated Icon */}
      <div className="relative z-10 w-8 h-8 rounded-full bg-[#412653]/70 border border-white/40 flex items-center justify-center shadow-inner group-hover:scale-110 transition-transform">
        <Play className="w-4 h-4 text-white fill-white translate-x-0.5" />
      </div>

      {/* Button Label */}
      <span className="relative z-10 font-extrabold tracking-wider text-white drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)] font-mono">
        {label}
      </span>

      {/* Glass Pill Indicator */}
      <span className="relative z-10 hidden sm:inline-flex items-center gap-1 text-[11px] px-3 py-1 rounded-full bg-white/15 border border-white/20 text-white uppercase font-mono tracking-widest backdrop-blur-md">
        <Sparkles className="w-3 h-3 text-[#D174D2] animate-pulse" />
        AI Engine
      </span>
    </button>
  );
}
