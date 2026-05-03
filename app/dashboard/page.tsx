'use client';

import Link from 'next/link';
import { TrendingUp, TrendingDown, CheckCircle, AlertTriangle, XCircle, PlusCircle, Loader2, Eye } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import PageWrapper from '@/components/layout/PageWrapper';
import StatusBadge from '@/components/ui/StatusBadge';
import { useGetAssessments } from '@/hooks/useAssessments';
import { formatDate, formatScore, getScoreColor } from '@/lib/utils';
import { RISK_FLAG_DESCRIPTIONS } from '@/lib/constants';
import { SkeletonMetricCard, SkeletonChart, SkeletonTable } from '@/components/ui/LoadingSkeleton';
import ErrorState from '@/components/ui/ErrorState';

export default function DashboardPage() {
  const { data: assessments = [], isLoading, error, refetch } = useGetAssessments();
  
  // Calculate stats
  const totalAssessments = assessments.length;
  const preApproved = assessments.filter((a) => a.recommendation === 'pre_approve').length;
  const needsVerification = assessments.filter((a) => a.recommendation === 'needs_verification').length;
  const rejected = assessments.filter((a) => a.recommendation === 'reject').length;
  const avgScore = assessments.length > 0 
    ? Math.round(assessments.reduce((sum, a) => sum + (a.csqs || 0), 0) / assessments.length)
    : 0;

  // Recent assessments (5 most recent)
  const recentAssessments = [...assessments]
    .sort((a, b) => new Date(b.createdAt || b.created_at).getTime() - new Date(a.createdAt || a.created_at).getTime())
    .slice(0, 5);

  // Donut chart data
  const chartData = [
    { name: 'Pre-Approved', value: preApproved, color: '#10B981' },
    { name: 'Needs Verification', value: needsVerification, color: '#F59E0B' },
    { name: 'Rejected', value: rejected, color: '#EF4444' },
  ].filter(item => item.value > 0);

  // Most common risk flag
  const riskFlagCounts: Record<string, number> = {};
  assessments.forEach(assessment => {
    if (assessment.riskFlags || assessment.risk_flags) {
      const flags = assessment.riskFlags || assessment.risk_flags || [];
      flags.forEach(flag => {
        const flagText = typeof flag === 'string' ? flag : flag.message;
        const key = flagText.toLowerCase().replace(/\s+/g, '_');
        riskFlagCounts[key] = (riskFlagCounts[key] || 0) + 1;
      });
    }
  });
  const mostCommonFlag = Object.entries(riskFlagCounts).sort((a, b) => b[1] - a[1])[0];

  if (isLoading) {
    return (
      <PageWrapper title="Dashboard" description="Overview of your kirana store assessments">
        {/* Skeleton Loading State */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <SkeletonMetricCard />
          <SkeletonMetricCard />
          <SkeletonMetricCard />
          <SkeletonMetricCard />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
          <div className="lg:col-span-3">
            <SkeletonTable rows={5} />
          </div>
          <div className="lg:col-span-2 space-y-6">
            <SkeletonChart />
            <SkeletonChart />
          </div>
        </div>
      </PageWrapper>
    );
  }

  if (error) {
    const isNetworkError = error.message === 'Network Error' || error.code === 'ECONNABORTED';
    
    return (
      <PageWrapper title="Dashboard" description="Overview of your kirana store assessments">
        <ErrorState
          type={isNetworkError ? 'network' : 'server'}
          title={isNetworkError ? 'Unable to Connect' : 'Server Error'}
          message={isNetworkError 
            ? 'Please check if the API server is running and try again.' 
            : 'Failed to load assessments. Please try again.'
          }
          onRetry={() => refetch()}
        />
      </PageWrapper>
    );
  }

  return (
    <PageWrapper title="Dashboard" description="Overview of your kirana store assessments">
      {/* Top Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Total Assessments */}
        <div className="bg-white rounded-card border border-gray-200 p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Assessments</p>
              <p className="text-3xl font-heading font-bold text-primary mt-2">{totalAssessments}</p>
            </div>
            <div className="flex items-center gap-1 text-success text-sm">
              <TrendingUp size={16} />
              <span>12%</span>
            </div>
          </div>
          <p className="text-xs text-gray-500">vs last month</p>
        </div>

        {/* Pre-Approved */}
        <div className="bg-white rounded-card border border-gray-200 p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm font-medium text-gray-600">Pre-Approved</p>
              <p className="text-3xl font-heading font-bold text-success mt-2">{preApproved}</p>
            </div>
            <CheckCircle className="text-success" size={24} />
          </div>
          <p className="text-xs text-gray-500">Ready for disbursement</p>
        </div>

        {/* Needs Verification */}
        <div className="bg-white rounded-card border border-gray-200 p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm font-medium text-gray-600">Needs Verification</p>
              <p className="text-3xl font-heading font-bold text-warning mt-2">{needsVerification}</p>
            </div>
            <AlertTriangle className="text-warning" size={24} />
          </div>
          <p className="text-xs text-gray-500">Requires manual review</p>
        </div>

        {/* Rejected */}
        <div className="bg-white rounded-card border border-gray-200 p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm font-medium text-gray-600">Rejected</p>
              <p className="text-3xl font-heading font-bold text-danger mt-2">{rejected}</p>
            </div>
            <XCircle className="text-danger" size={24} />
          </div>
          <p className="text-xs text-gray-500">Did not meet criteria</p>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-8">
        {/* Left: Recent Assessments Table (60%) */}
        <div className="lg:col-span-3 bg-white rounded-card border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-heading font-bold text-primary">Recent Assessments</h2>
            <Link href="/admin" className="text-accent hover:text-accent/80 text-sm font-medium">
              View All →
            </Link>
          </div>

          {recentAssessments.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b border-gray-200">
                  <tr>
                    <th className="text-left text-xs font-medium text-gray-600 uppercase pb-3">Date</th>
                    <th className="text-left text-xs font-medium text-gray-600 uppercase pb-3">Store Name</th>
                    <th className="text-left text-xs font-medium text-gray-600 uppercase pb-3">Location</th>
                    <th className="text-left text-xs font-medium text-gray-600 uppercase pb-3">Score</th>
                    <th className="text-left text-xs font-medium text-gray-600 uppercase pb-3">Recommendation</th>
                    <th className="text-left text-xs font-medium text-gray-600 uppercase pb-3">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {recentAssessments.map((assessment) => {
                    const csqs = assessment.csqs || 0;
                    const scoreColor = getScoreColor(csqs);
                    const storeName = assessment.storeName || assessment.store_name || 'Unknown Store';
                    const address = assessment.address || 'Unknown Location';
                    const location = address.includes(',') ? address.split(',').slice(-2).join(',').trim() : address;
                    const createdAt = assessment.createdAt || assessment.created_at;
                    
                    return (
                      <tr key={assessment.id} className="hover:bg-gray-50">
                        <td className="py-4 text-sm text-gray-600">
                          {formatDate(createdAt)}
                        </td>
                        <td className="py-4">
                          <p className="font-medium text-gray-900">{storeName}</p>
                        </td>
                        <td className="py-4 text-sm text-gray-600">
                          {location}
                        </td>
                        <td className="py-4">
                          <span 
                            className="inline-flex items-center px-2.5 py-0.5 rounded-badge text-xs font-bold"
                            style={{ 
                              backgroundColor: `${scoreColor}20`,
                              color: scoreColor 
                            }}
                          >
                            {csqs}
                          </span>
                        </td>
                        <td className="py-4">
                          <StatusBadge status={assessment.recommendation} size="sm" />
                        </td>
                        <td className="py-4">
                          <Link
                            href={`/assess/${assessment.id}`}
                            className="inline-flex items-center gap-1 text-accent hover:text-accent/80 text-sm font-medium"
                          >
                            <Eye size={16} />
                            View
                          </Link>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">No assessments yet</p>
            </div>
          )}
        </div>

        {/* Right: Quick Stats Panel (40%) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Donut Chart */}
          <div className="bg-white rounded-card border border-gray-200 p-6">
            <h3 className="text-lg font-heading font-semibold text-primary mb-4">
              Recommendation Breakdown
            </h3>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-center text-gray-500 py-8">No data available</p>
            )}
          </div>

          {/* Average CSQS Score */}
          <div className="bg-white rounded-card border border-gray-200 p-6">
            <h3 className="text-lg font-heading font-semibold text-primary mb-4">
              Average CSQS Score
            </h3>
            <div className="text-center">
              <p 
                className="text-5xl font-heading font-bold mb-2"
                style={{ color: getScoreColor(avgScore) }}
              >
                {avgScore}
              </p>
              <p className="text-sm text-gray-600">Across all assessments</p>
            </div>
          </div>

          {/* Most Common Risk Flag */}
          {mostCommonFlag && (
            <div className="bg-white rounded-card border border-gray-200 p-6">
              <h3 className="text-lg font-heading font-semibold text-primary mb-4">
                Most Common Risk Flag
              </h3>
              <div className="flex items-start gap-3">
                <AlertTriangle className="text-warning flex-shrink-0 mt-1" size={20} />
                <div>
                  <p className="font-medium text-gray-900 mb-1">
                    {mostCommonFlag[0].replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </p>
                  <p className="text-sm text-gray-600">
                    Detected in {mostCommonFlag[1]} assessment{mostCommonFlag[1] > 1 ? 's' : ''}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Floating CTA Button */}
      <Link
        href="/assess"
        className="fixed bottom-8 right-8 bg-accent hover:bg-accent/90 text-white px-6 py-4 rounded-card shadow-2xl flex items-center gap-2 font-medium transition-all hover:scale-105 z-50"
      >
        <PlusCircle size={20} />
        New Assessment
      </Link>
    </PageWrapper>
  );
}
