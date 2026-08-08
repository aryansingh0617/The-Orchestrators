'use client';

import React from 'react';

export function AnimatedBackground() {
  return (
    <div className="fixed inset-0 w-full h-full -z-10 pointer-events-none overflow-hidden">
      {/* Full-Screen Scaled Video Background */}
      <video
        autoPlay
        loop
        muted
        playsInline
        className="fixed inset-0 w-full h-full object-cover -z-10 pointer-events-none"
      >
        <source src="/Luma-Dot-Background (1).mp4" type="video/mp4" />
      </video>

      {/* Subtle Ambient Color Overlay Tint for contrast */}
      <div className="fixed inset-0 bg-[#443199]/20 backdrop-brightness-[0.85] -z-10 pointer-events-none" />
    </div>
  );
}
