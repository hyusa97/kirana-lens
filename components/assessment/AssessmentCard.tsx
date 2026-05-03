import Link from 'next/link';
import { MapPin, Calendar } from 'lucide-react';
import { formatDate, formatRupees } from '@/lib/utils';
import { TIER_COLORS } from '@/lib/constants';
import StatusBadge from '@/components/ui/StatusBadge';
import type { Assessment } from '@/lib/types';

interface AssessmentCardProps {
  assessment: Assessment;
}

export default function AssessmentCard({ assessment }: AssessmentCardProps) {
  const item = assessment as any;
  const storeName = item.storeName || item.store_name || 'Unknown Store';
  const address = item.address || 'Unknown Location';
  const storeTier = item.storeTier || item.store_tier || '-';
  const confidence = Number(item.confidenceScore || item.confidence_score || 0);
  const monthlyRevenueMin = item.monthlyRevenueMin || item.monthly_revenue_min || 0;
  const monthlyRevenueMax = item.monthlyRevenueMax || item.monthly_revenue_max || 0;
  const createdAt = item.createdAt || item.created_at;

  return (
    <Link href={`/assess/${assessment.id}`}>
      <div className="bg-white rounded-card border border-gray-200 p-6 hover:shadow-lg transition-shadow cursor-pointer">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="font-heading font-semibold text-lg text-primary mb-1">
              {storeName}
            </h3>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <MapPin size={14} />
              <span className="truncate max-w-xs">{address}</span>
            </div>
          </div>
          <span
            className={`inline-flex items-center px-2.5 py-0.5 rounded-badge text-xs font-medium border ${
              TIER_COLORS[storeTier] || 'bg-gray-100 text-gray-800 border-gray-300'
            }`}
          >
            Tier {storeTier}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-xs text-gray-500 mb-1">CSQS Score</p>
            <p className="text-2xl font-heading font-bold text-primary">{assessment.csqs || 'Legacy'}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">Confidence</p>
            <p className="text-2xl font-heading font-bold text-primary">
              {Math.round(confidence <= 1 ? confidence * 100 : confidence)}%
            </p>
          </div>
        </div>

        <div className="mb-4">
          <p className="text-xs text-gray-500 mb-1">Monthly Revenue Range</p>
          <p className="text-sm font-medium text-gray-900">
            {formatRupees(monthlyRevenueMin)} - {formatRupees(monthlyRevenueMax)}
          </p>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-gray-200">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Calendar size={14} />
            <span>{formatDate(createdAt)}</span>
          </div>
          <StatusBadge status={assessment.recommendation} size="sm" />
        </div>
      </div>
    </Link>
  );
}
