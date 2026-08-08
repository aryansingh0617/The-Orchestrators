'use client';

import React from 'react';

export function AnimatedBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden bg-[#070a13]">
      {/* Orb 1: Neon Pink (Top-Left) */}
      <div className="absolute top-[-10%] left-[-10%] w-[55vw] h-[55vw] rounded-full opacity-70 blur-[90px] animate-orb-1 bg-[radial-gradient(circle,rgba(236,72,153,0.55)_0%,rgba(219,39,119,0.2)_50%,transparent_70%)]" />

      {/* Orb 2: Soft Violet (Top-Right) */}
      <div className="absolute top-[-5%] right-[-10%] w-[50vw] h-[50vw] rounded-full opacity-70 blur-[90px] animate-orb-2 bg-[radial-gradient(circle,rgba(139,92,246,0.55)_0%,rgba(124,58,237,0.2)_50%,transparent_70%)]" />

      {/* Orb 3: Warm Orange (Bottom-Left) */}
      <div className="absolute bottom-[-10%] left-[-5%] w-[52vw] h-[52vw] rounded-full opacity-65 blur-[100px] animate-orb-3 bg-[radial-gradient(circle,rgba(249,115,22,0.5)_0%,rgba(234,88,12,0.18)_50%,transparent_70%)]" />

      {/* Orb 4: Cyan / Rose Glow (Center-Right) */}
      <div className="absolute top-[40%] right-[15%] w-[45vw] h-[45vw] rounded-full opacity-60 blur-[95px] animate-orb-4 bg-[radial-gradient(circle,rgba(6,182,212,0.45)_0%,rgba(99,102,241,0.18)_50%,transparent_70%)]" />

      {/* Fine Mesh / Grid Overlay for depth */}
      <div 
        className="absolute inset-0 opacity-[0.03]" 
        style={{
          backgroundImage: `radial-gradient(rgba(255, 255, 255, 0.4) 1px, transparent 1px)`,
          backgroundSize: '32px 32px'
        }}
      />
    </div>
  );
}
