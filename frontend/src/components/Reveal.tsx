'use client';

import React from 'react';
import { useInView } from '@/lib/useInView';

interface RevealProps {
  children: React.ReactNode;
  delayMs?: number;
  durationMs?: number;
  className?: string;
}

export function Reveal({
  children,
  delayMs = 0,
  durationMs = 300,
  className = '',
}: RevealProps) {
  const { ref, inView } = useInView({ threshold: 0.15 });

  return (
    <div
      ref={ref}
      style={{
        transitionDelay: `${delayMs}ms`,
        transitionDuration: `${durationMs}ms`,
      }}
      className={`transition-all ease-out will-change-[opacity,transform] ${
        inView
          ? 'opacity-100 translate-y-0 pointer-events-auto'
          : 'opacity-0 translate-y-4'
      } ${className}`}
    >
      {children}
    </div>
  );
}
