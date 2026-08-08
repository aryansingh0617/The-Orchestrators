'use client';

import React, { useState, useMemo } from 'react';
import { getCandidates, getCohortInfo, Candidate } from '@/lib/candidates';
import { HeroSection } from '@/components/HeroSection';
import { CandidateCard } from '@/components/CandidateCard';
import { CandidateModal } from '@/components/CandidateModal';
import { Layers, AlertCircle, Sparkles } from 'lucide-react';

export default function LandingPage() {
  const allCandidates = useMemo(() => getCandidates(), []);
  const cohortInfo = useMemo(() => {
    const raw = getCohortInfo();
    return {
      cohort: raw.cohort,
      modulesCount: raw.modules.length,
      daysCount: raw.days.length,
    };
  }, []);

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('ALL');
  const [activeCandidate, setActiveCandidate] = useState<Candidate | null>(null);

  const filteredCandidates = useMemo(() => {
    return allCandidates.filter((c) => {
      // Search match
      const matchesSearch =
        c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.jobRole.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.education.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.id.toLowerCase().includes(searchQuery.toLowerCase());

      // Filter match
      let matchesFilter = true;
      if (selectedFilter === 'TOP_PERFORMER') {
        matchesFilter = c.overallScore >= 85;
      } else if (selectedFilter === 'HIGH_ACCURACY') {
        matchesFilter = c.signals.missionsFirstTry >= 15;
      } else if (selectedFilter === 'HIGH_CONSISTENCY') {
        matchesFilter = c.signals.commitDays >= 25;
      }

      return matchesSearch && matchesFilter;
    });
  }, [allCandidates, searchQuery, selectedFilter]);

  return (
    <main className="min-h-screen p-4 sm:p-8 lg:p-12 max-w-7xl mx-auto relative z-10">
      {/* Hero Section */}
      <HeroSection
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        selectedFilter={selectedFilter}
        onFilterChange={setSelectedFilter}
        totalCandidates={allCandidates.length}
        cohortInfo={cohortInfo}
      />

      {/* Candidate Grid Section */}
      <section className="mb-12">
        <div className="flex items-center justify-between mb-6 px-1">
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-cyan-400" />
            <h2 className="text-xl font-black text-white uppercase tracking-wider font-mono glass-text-glow">
              Candidate Assessment Dossiers
            </h2>
          </div>
          <span className="font-mono text-xs text-cyan-200 bg-cyan-500/10 px-3.5 py-1 rounded-full border border-cyan-500/20 backdrop-blur-md">
            Showing {filteredCandidates.length} of {allCandidates.length}
          </span>
        </div>

        {filteredCandidates.length === 0 ? (
          <div className="glass-panel p-12 text-center flex flex-col items-center justify-center">
            <AlertCircle className="w-12 h-12 text-amber-400 mb-3" />
            <h3 className="text-lg font-bold text-slate-200">
              No Candidates Matched Your Query
            </h3>
            <p className="text-xs text-slate-400 mt-1 max-w-md">
              Try adjusting your search keywords or filter criteria to inspect available candidate dossiers.
            </p>
            <button
              onClick={() => {
                setSearchQuery('');
                setSelectedFilter('ALL');
              }}
              type="button"
              className="glass-secondary-btn text-xs font-mono font-bold px-4 py-2 rounded-xl mt-4 text-cyan-300"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCandidates.map((candidate) => (
              <CandidateCard
                key={candidate.id}
                candidate={candidate}
                onSelect={setActiveCandidate}
              />
            ))}
          </div>
        )}
      </section>

      {/* Glassmorphic Telemetry Footer */}
      <footer className="glass-panel p-5 text-center text-xs font-mono text-slate-400 border border-white/10">
        <p className="flex items-center justify-center gap-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          CHIMERA AI ENGINEERING ASSESSMENT OS // COHORT TELEMETRY ENGINE ONLINE
        </p>
      </footer>

      {/* Candidate Modal */}
      <CandidateModal
        candidate={activeCandidate}
        onClose={() => setActiveCandidate(null)}
      />
    </main>
  );
}
