import { formatRupeeRange } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

interface RangeCardProps {
  title: string;
  min?: number;
  max?: number;
  value?: string;
  subtitle?: string;
  icon?: LucideIcon;
  iconColor?: string;
}

export default function RangeCard({
  title,
  min,
  max,
  value,
  subtitle,
  icon: Icon,
  iconColor = 'text-accent',
}: RangeCardProps) {
  return (
    <div className="bg-white rounded-card border border-gray-200 p-6">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
        {Icon && <Icon className={`${iconColor}`} size={20} />}
      </div>
      <p className="text-2xl font-heading font-bold text-primary">
        {value || formatRupeeRange(min || 0, max || 0)}
      </p>
    </div>
  );
}
