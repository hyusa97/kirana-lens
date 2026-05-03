'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowUpDown, Eye } from 'lucide-react';
import { formatDate, formatRupees } from '@/lib/utils';
import { TIER_COLORS } from '@/lib/constants';
import StatusBadge from '@/components/ui/StatusBadge';
import type { Assessment } from '@/lib/types';

interface AssessmentTableProps {
  assessments: Assessment[];
}

type SortField = 'createdAt' | 'csqs' | 'storeName';
type SortDirection = 'asc' | 'desc';

export default function AssessmentTable({ assessments }: AssessmentTableProps) {
  const [sortField, setSortField] = useState<SortField>('createdAt');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const sortedAssessments = [...assessments].sort((a, b) => {
    const getValue = (item: any) => item[sortField] || item[sortField === 'createdAt' ? 'created_at' : sortField === 'storeName' ? 'store_name' : sortField];
    let aVal: any = getValue(a);
    let bVal: any = getValue(b);

    if (sortField === 'createdAt') {
      aVal = new Date(aVal).getTime();
      bVal = new Date(bVal).getTime();
    }

    if (sortDirection === 'asc') {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });

  return (
    <div className="bg-white rounded-card border border-gray-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left">
                <button
                  onClick={() => handleSort('storeName')}
                  className="flex items-center gap-2 text-xs font-medium text-gray-700 uppercase tracking-wider hover:text-primary"
                >
                  Store Name
                  <ArrowUpDown size={14} />
                </button>
              </th>
              <th className="px-6 py-3 text-left">
                <button
                  onClick={() => handleSort('createdAt')}
                  className="flex items-center gap-2 text-xs font-medium text-gray-700 uppercase tracking-wider hover:text-primary"
                >
                  Date
                  <ArrowUpDown size={14} />
                </button>
              </th>
              <th className="px-6 py-3 text-left">
                <button
                  onClick={() => handleSort('csqs')}
                  className="flex items-center gap-2 text-xs font-medium text-gray-700 uppercase tracking-wider hover:text-primary"
                >
                  CSQS
                  <ArrowUpDown size={14} />
                </button>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Tier
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Monthly Revenue
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Recommendation
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {sortedAssessments.map((assessment) => (
              <tr key={assessment.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4">
                  <div>
                    <p className="font-medium text-gray-900">{(assessment as any).storeName || assessment.store_name || 'Unknown Store'}</p>
                    <p className="text-sm text-gray-500 truncate max-w-xs">{assessment.address}</p>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-700">
                  {formatDate((assessment as any).createdAt || assessment.created_at)}
                </td>
                <td className="px-6 py-4">
                  <span className="text-lg font-heading font-bold text-primary">
                    {assessment.csqs}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-badge text-xs font-medium border ${
                      TIER_COLORS[(assessment as any).storeTier || assessment.store_tier || ''] || 'bg-gray-100 text-gray-800 border-gray-300'
                    }`}
                  >
                    Tier {(assessment as any).storeTier || assessment.store_tier || '-'}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-700">
                  {formatRupees((assessment as any).monthlyRevenueMin || assessment.monthly_revenue_min || 0)} - {formatRupees((assessment as any).monthlyRevenueMax || assessment.monthly_revenue_max || 0)}
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={assessment.recommendation} size="sm" />
                </td>
                <td className="px-6 py-4">
                  <Link
                    href={`/assess/${assessment.id}`}
                    className="inline-flex items-center gap-2 text-accent hover:text-accent/80 transition-colors"
                  >
                    <Eye size={16} />
                    <span className="text-sm font-medium">View</span>
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
