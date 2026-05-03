import { AlertTriangle, AlertCircle, Info } from 'lucide-react';
import type { RiskFlag } from '@/lib/types';

interface RiskFlagCardProps {
  flag: RiskFlag;
}

export default function RiskFlagCard({ flag }: RiskFlagCardProps) {
  const icons = {
    high: <AlertTriangle size={20} />,
    medium: <AlertCircle size={20} />,
    low: <Info size={20} />,
  };

  const colors = {
    high: 'bg-danger/10 border-danger text-danger',
    medium: 'bg-warning/10 border-warning text-warning',
    low: 'bg-blue-50 border-blue-300 text-blue-700',
  };

  return (
    <div className={`rounded-input border p-4 flex items-start gap-3 ${colors[flag.type]}`}>
      <div className="flex-shrink-0 mt-0.5">{icons[flag.type]}</div>
      <div>
        <p className="font-medium text-sm">{flag.message}</p>
        <p className="text-xs opacity-80 mt-1">Severity: {flag.severity}/5</p>
      </div>
    </div>
  );
}
