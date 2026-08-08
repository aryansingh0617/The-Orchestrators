'use client';

import React from 'react';

export function AnimatedBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden bg-[#412653]">
      {/* Orb 1: Vibrant Coral #E0563F (Top-Left) */}
      <div className="absolute top-[-15%] left-[-10%] w-[60vw] h-[60vw] rounded-full opacity-65 blur-[100px] animate-organic-1 bg-[radial-gradient(circle,#E0563F_0%,rgba(224,86,63,0.2)_50%,transparent_70%)]" />

      {/* Orb 2: Light Orchid #D174D2 (Top-Right) */}
      <div className="absolute top-[-10%] right-[-10%] w-[55vw] h-[55vw] rounded-full opacity-65 blur-[100px] animate-organic-2 bg-[radial-gradient(circle,#D174D2_0%,rgba(209,116,210,0.2)_50%,transparent_70%)]" />

      {/* Orb 3: Secondary Slate #3F567F (Bottom-Left) */}
      <div className="absolute bottom-[-15%] left-[-5%] w-[58vw] h-[58vw] rounded-full opacity-70 blur-[110px] animate-organic-3 bg-[radial-gradient(circle,#3F567F_0%,rgba(63,86,127,0.25)_50%,transparent_70%)]" />

      {/* Orb 4: Center Glow Blend (Coral & Orchid) */}
      <div className="absolute top-[35%] right-[20%] w-[48vw] h-[48vw] rounded-full opacity-50 blur-[95px] animate-organic-1 bg-[radial-gradient(circle,#E0563F_0%,#D174D2_40%,transparent_70%)]" />

      {/* Organic Subtle Grain Noise Overlay */}
      <div 
        className="absolute inset-0 opacity-[0.02]" 
        style={{
          backgroundImage: `radial-gradient(#FFFFFF 1px, transparent 1px)`,
          backgroundSize: '28px 28px'
        }}
      />
    </div>
  );
}
