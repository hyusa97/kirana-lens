import React from 'react';

interface LoadingSkeletonProps {
  className?: string;
}

export function SkeletonCard({ className = '' }: LoadingSkeletonProps) {
  return (
    <div className={`bg-white rounded-card border border-gray-200 p-6 ${className}`}>
      <div className="animate-pulse space-y-4">
        <div className="h-4 bg-gray-200 rounded w-1/3"></div>
        <div className="h-8 bg-gray-200 rounded w-1/2"></div>
        <div className="h-3 bg-gray-200 rounded w-2/3"></div>
      </div>
    </div>
  );
}

export function SkeletonTable({ rows = 5 }: { rows?: number }) {
  return (
    <div className="bg-white rounded-card border border-gray-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              {[1, 2, 3, 4, 5, 6, 7].map((i) => (
                <th key={i} className="px-6 py-3">
                  <div className="h-3 bg-gray-200 rounded animate-pulse"></div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {Array.from({ length: rows }).map((_, i) => (
              <tr key={i}>
                {[1, 2, 3, 4, 5, 6, 7].map((j) => (
                  <td key={j} className="px-6 py-4">
                    <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export function SkeletonGauge() {
  return (
    <div className="flex flex-col items-center justify-center">
      <div className="w-32 h-32 rounded-full bg-gray-200 animate-pulse"></div>
      <div className="mt-4 h-4 bg-gray-200 rounded w-24 animate-pulse"></div>
    </div>
  );
}

export function SkeletonRangeCard() {
  return (
    <div className="bg-white rounded-card border border-gray-200 p-6">
      <div className="animate-pulse space-y-3">
        <div className="flex items-center justify-between">
          <div className="h-3 bg-gray-200 rounded w-1/2"></div>
          <div className="w-5 h-5 bg-gray-200 rounded-full"></div>
        </div>
        <div className="h-6 bg-gray-200 rounded w-3/4"></div>
      </div>
    </div>
  );
}

export function SkeletonMetricCard() {
  return (
    <div className="bg-white rounded-card border border-gray-200 p-6">
      <div className="animate-pulse space-y-4">
        <div className="flex items-start justify-between">
          <div className="space-y-2 flex-1">
            <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          </div>
          <div className="w-6 h-6 bg-gray-200 rounded"></div>
        </div>
        <div className="h-2 bg-gray-200 rounded w-1/4"></div>
      </div>
    </div>
  );
}

export function SkeletonChart() {
  return (
    <div className="bg-white rounded-card border border-gray-200 p-6">
      <div className="animate-pulse space-y-4">
        <div className="h-4 bg-gray-200 rounded w-1/3"></div>
        <div className="h-48 bg-gray-200 rounded"></div>
      </div>
    </div>
  );
}
