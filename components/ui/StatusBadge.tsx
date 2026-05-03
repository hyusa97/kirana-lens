import { RECOMMENDATION_COLORS, RECOMMENDATION_LABELS } from '@/lib/constants';
import type { RecommendationType } from '@/lib/types';

interface StatusBadgeProps {
  status: RecommendationType;
  size?: 'sm' | 'md' | 'lg';
}

export default function StatusBadge({ status, size = 'md' }: StatusBadgeProps) {
  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5',
    lg: 'text-base px-4 py-2',
  };

  return (
    <span
      className={`inline-flex items-center rounded-badge border font-medium ${RECOMMENDATION_COLORS[status]} ${sizeClasses[size]}`}
    >
      {RECOMMENDATION_LABELS[status]}
    </span>
  );
}
