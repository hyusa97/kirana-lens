import { getScoreColor } from '@/lib/utils';

interface ConfidenceBarProps {
  score: number;
  label?: string;
}

export default function ConfidenceBar({ score, label = 'Confidence Score' }: ConfidenceBarProps) {
  const scoreColor = getScoreColor(score);
  
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className="text-sm font-bold text-primary">{Math.round(score)}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
        <div
          className="h-full transition-all duration-500 ease-out rounded-full"
          style={{ 
            width: `${score}%`,
            backgroundColor: scoreColor
          }}
        />
      </div>
    </div>
  );
}
