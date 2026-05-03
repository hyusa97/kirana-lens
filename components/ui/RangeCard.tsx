import { formatRupeeRange } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

interface RangeCardProps {
  title: string;
  min: number;
  max: number;
  icon: LucideIcon;
  iconColor?: string;
}

export default function RangeCard({
  title,
  min,
  max,
  icon: Icon,
  iconColor = 'text-accent',
}: RangeCardProps) {
  return (
    <div className="bg-white rounded-card border border-gray-200 p-6">
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-sm font-medium text-gray-600">{title}</h3>
        <Icon className={`${iconColor}`} size={20} />
      </div>
      <p className="text-2xl font-heading font-bold text-primary">
        {formatRupeeRange(min, max)}
      </p>
    </div>
  );
}
