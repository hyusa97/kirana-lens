'use client';

import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { SIGNAL_LABELS } from '@/lib/constants';
import { getScoreColor } from '@/lib/utils';
import type { SignalBreakdown as SignalBreakdownType } from '@/lib/types';

interface SignalBreakdownProps {
  signals: SignalBreakdownType;
}

export default function SignalBreakdown({ signals }: SignalBreakdownProps) {
  const [expandedSection, setExpandedSection] = useState<'visual' | 'geo' | null>('visual');

  const toggleSection = (section: 'visual' | 'geo') => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  const renderFeatureScore = (key: string, value: number) => {
    const scoreColor = getScoreColor(value);
    const signalInfo = SIGNAL_LABELS[key];
    
    return (
      <div key={key} className="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
        <div className="flex-1">
          <span className="text-sm font-medium text-gray-900">{signalInfo?.label || key}</span>
          {signalInfo?.hindiLabel && (
            <span className="text-xs text-gray-500 ml-2">({signalInfo.hindiLabel})</span>
          )}
        </div>
        <span 
          className="text-sm font-bold ml-4"
          style={{ color: scoreColor }}
        >
          {Math.round(value)}
        </span>
      </div>
    );
  };

  return (
    <div className="space-y-3">
      {/* Visual Features */}
      <div className="bg-white rounded-card border border-gray-200 overflow-hidden">
        <button
          onClick={() => toggleSection('visual')}
          className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
        >
          <div>
            <h3 className="font-heading font-semibold text-primary text-left">Visual Features</h3>
            <p className="text-xs text-gray-500 text-left">7 signals from store imagery</p>
          </div>
          {expandedSection === 'visual' ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        {expandedSection === 'visual' && (
          <div className="px-6 pb-4">
            {Object.entries(signals.visual).map(([key, value]) => renderFeatureScore(key, value))}
          </div>
        )}
      </div>

      {/* Geo Features */}
      <div className="bg-white rounded-card border border-gray-200 overflow-hidden">
        <button
          onClick={() => toggleSection('geo')}
          className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
        >
          <div>
            <h3 className="font-heading font-semibold text-primary text-left">Geo Features</h3>
            <p className="text-xs text-gray-500 text-left">5 signals from location data</p>
          </div>
          {expandedSection === 'geo' ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        {expandedSection === 'geo' && (
          <div className="px-6 pb-4">
            {Object.entries(signals.geo).map(([key, value]) => renderFeatureScore(key, value))}
          </div>
        )}
      </div>
    </div>
  );
}
