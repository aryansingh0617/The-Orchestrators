import type { Metadata } from 'next';
import './globals.css';
import { AnimatedBackground } from '@/components/AnimatedBackground';
import { TeamCredits } from '@/components/TeamCredits';

export const metadata: Metadata = {
  title: 'CHIMERA // AI Engineering Assessment OS',
  description:
    'High-fidelity physical simulation engine for evaluating autonomous agent architects, LLM system engineers, and GPU infrastructure talent.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased selection:bg-pink-500 selection:text-white relative">
        <AnimatedBackground />
        {children}
        <TeamCredits />
      </body>
    </html>
  );
}
