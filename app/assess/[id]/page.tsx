'use client';

import { notFound } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, MapPin, Calendar, DollarSign, TrendingUp, Building, Loader2, Download, AlertTriangle } from 'lucide-react';
import PageWrapper from '@/components/layout/PageWrapper';
import ScoreGauge from '@/components/ui/ScoreGauge';
import RangeCard from '@/components/ui/RangeCard';
import ConfidenceBar from '@/components/ui/ConfidenceBar';
import StatusBadge from '@/components/ui/StatusBadge';
import RiskFlagCard from '@/components/ui/RiskFlagCard';
import SignalBreakdown from '@/components/ui/SignalBreakdown';
import { useGetAssessment, useDownloadReport } from '@/hooks/useAssessments';
import { formatDate, getTierLabel, getConfidenceLabel, formatRupeeRange } from '@/lib/utils';
import { RECOMMENDATION_CONFIG } from '@/lib/constants';
import { SkeletonGauge, SkeletonRangeCard, SkeletonCard } from '@/components/ui/LoadingSkeleton';

export default function AssessmentResultPage({ params }: { params: { id: string } }) {
  const { data: assessment, isLoading, error } = useGetAssessment(params.id);
  const downloadReport = useDownloadReport();

  const handleDownloadReport = () => {
    downloadReport.mutate(params.id);
  };

  if (isLoading) {
    return (
      <PageWrapper>
        <div className="max-w-7xl mx-auto">
          {/* Header Skeleton */}
          <div className="bg-white rounded-card border border-gray-200 p-6 mb-6">
            <div className="animate-pulse space-y-4">
              <div className="h-8 bg-gray-200 rounded w-1/3"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>

          {/* Hero Metrics Skeleton */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            <div className="bg-white rounded-card border border-gray-200 p-6">
              <SkeletonGauge />
            </div>
            <SkeletonRangeCard />
            <SkeletonRangeCard />
            <SkeletonRangeCard />
          </div>

          {/* Other sections skeleton */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <SkeletonCard />
            <SkeletonCard />
          </div>
        </div>
      </PageWrapper>
    );
  }

  if (error || !assessment) {
    notFound();
  }

  const recommendationConfig = RECOMMENDATION_CONFIG[assessment.recommendation || 'needs_verification'];
  const confidenceScore = assessment.confidenceScore || assessment.confidence_score || 0;
  const confidenceLabel = getConfidenceLabel(confidenceScore);
  const storeName = assessment.storeName || assessment.store_name || 'Unknown Store';
  const address = assessment.address || 'Unknown Location';
  const createdAt = assessment.createdAt || assessment.created_at;
  const csqs = assessment.csqs || 0;
  const storeTier = assessment.storeTier || assessment.store_tier;
  const dailySalesMin = assessment.dailySalesMin || assessment.daily_sales_min || 0;
  const dailySalesMax = assessment.dailySalesMax || assessment.daily_sales_max || 0;
  const monthlyRevenueMin = assessment.monthlyRevenueMin || assessment.monthly_revenue_min || 0;
  const monthlyRevenueMax = assessment.monthlyRevenueMax || assessment.monthly_revenue_max || 0;
  const monthlyIncomeMin = assessment.monthlyIncomeMin || assessment.monthly_income_min || 0;
  const monthlyIncomeMax = assessment.monthlyIncomeMax || assessment.monthly_income_max || 0;
  const riskFlags = assessment.riskFlags || assessment.risk_flags || [];
  const signalBreakdown = assessment.signalBreakdown || assessment.signal_breakdown;
  const imageUrls = assessment.imageUrls || assessment.image_urls || [];

  return (
    <PageWrapper>
      <div className="max-w-7xl mx-auto">
        {/* Header Bar */}
        <div className="bg-white rounded-card border border-gray-200 p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <Link
                href="/admin"
                className="inline-flex items-center gap-2 text-accent hover:text-accent/80 mb-3 text-sm"
              >
                <ArrowLeft size={16} />
                Back to All Assessments
              </Link>
              <h1 className="text-3xl font-heading font-bold text-primary mb-2">
                {storeName}
              </h1>
              <div className="flex items-center gap-4 text-gray-600 text-sm">
                <div className="flex items-center gap-2">
                  <MapPin size={16} />
                  <span>{address}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar size={16} />
                  <span>{formatDate(createdAt)}</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <StatusBadge status={assessment.recommendation} size="lg" />
              <button 
                onClick={handleDownloadReport}
                disabled={downloadReport.isPending}
                className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-input hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {downloadReport.isPending ? (
                  <>
                    <Loader2 size={16} className="animate-spin" />
                    <span className="text-sm font-medium">Downloading...</span>
                  </>
                ) : (
                  <>
                    <Download size={16} />
                    <span className="text-sm font-medium">Download Report</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* ROW 1: Hero Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          {/* CSQS Score */}
          <div className="bg-white rounded-card border border-gray-200 p-6 flex flex-col items-center justify-center">
            <ScoreGauge score={csqs} label="CSQS Score" size="lg" />
            <div className="mt-4 text-center">
              <p className="text-sm text-gray-600 mb-1">Store Tier</p>
              <p className="text-lg font-heading font-bold text-primary">
                {getTierLabel(storeTier)}
              </p>
            </div>
          </div>

          {/* Daily Sales Range */}
          <div className="bg-white rounded-card border border-gray-200 p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-sm font-medium text-gray-600 mb-1">Daily Sales Range</h3>
                <p className="text-xs text-gray-500">रोज़ की बिक्री</p>
              </div>
              <DollarSign className="text-accent" size={20} />
            </div>
            <p className="text-2xl font-heading font-bold text-primary">
              {formatRupeeRange(dailySalesMin, dailySalesMax)}
            </p>
          </div>

          {/* Monthly Revenue */}
          <div className="bg-white rounded-card border border-gray-200 p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-sm font-medium text-gray-600 mb-1">Monthly Revenue</h3>
                <p className="text-xs text-gray-500">मासिक राजस्व</p>
              </div>
              <TrendingUp className="text-accent" size={20} />
            </div>
            <p className="text-2xl font-heading font-bold text-primary">
              {formatRupeeRange(monthlyRevenueMin, monthlyRevenueMax)}
            </p>
          </div>

          {/* Monthly Income */}
          <div className="bg-white rounded-card border border-gray-200 p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-sm font-medium text-gray-600 mb-1">Monthly Income</h3>
                <p className="text-xs text-gray-500">मासिक आय</p>
              </div>
              <Building className="text-accent" size={20} />
            </div>
            <p className="text-2xl font-heading font-bold text-primary">
              {formatRupeeRange(monthlyIncomeMin, monthlyIncomeMax)}
            </p>
          </div>
        </div>

        {/* ROW 2: Confidence & Recommendation */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Confidence Score */}
          <div className="bg-white rounded-card border border-gray-200 p-6">
            <h3 className="text-lg font-heading font-semibold text-primary mb-4">
              Confidence Score
            </h3>
            <ConfidenceBar score={confidenceScore} label="Model Confidence" />
            <div className="mt-4 flex items-center justify-between">
              <span className="text-sm text-gray-600">Confidence Level:</span>
              <span className={`text-sm font-bold ${
                confidenceLabel === 'High' ? 'text-success' :
                confidenceLabel === 'Medium' ? 'text-warning' : 'text-danger'
              }`}>
                {confidenceLabel}
              </span>
            </div>
            <p className="text-xs text-gray-600 mt-3">
              {confidenceLabel === 'High' && 'High confidence in the assessment. All signals are strong and consistent.'}
              {confidenceLabel === 'Medium' && 'Moderate confidence. Some signals may require verification.'}
              {confidenceLabel === 'Low' && 'Low confidence. Manual verification strongly recommended.'}
            </p>
          </div>

          {/* Recommendation */}
          <div className="bg-white rounded-card border border-gray-200 p-6">
            <h3 className="text-lg font-heading font-semibold text-primary mb-4">
              Recommendation
            </h3>
            <div className="flex items-center gap-4 mb-4">
              <div 
                className="w-16 h-16 rounded-full flex items-center justify-center"
                style={{ backgroundColor: recommendationConfig.bgColor }}
              >
                {assessment.recommendation === 'pre_approve' && '✓'}
                {assessment.recommendation === 'needs_verification' && '!'}
                {assessment.recommendation === 'reject' && '✗'}
              </div>
              <div className="flex-1">
                <StatusBadge status={assessment.recommendation} size="lg" />
              </div>
            </div>
            <p className="text-sm text-gray-700 leading-relaxed">
              {recommendationConfig.description}
            </p>
            <div className="mt-4 p-3 bg-gray-50 rounded-input">
              <p className="text-xs font-medium text-gray-700">Next Action:</p>
              <p className="text-xs text-gray-600 mt-1">
                {assessment.recommendation === 'pre_approve' && 'Proceed with loan disbursement process. All criteria met.'}
                {assessment.recommendation === 'needs_verification' && 'Schedule field visit for manual verification of flagged items.'}
                {assessment.recommendation === 'reject' && 'Do not proceed with loan. Store does not meet minimum criteria.'}
              </p>
            </div>
          </div>
        </div>

        {/* ROW 3: Risk Flags */}
        {riskFlags.length > 0 && (
          <div className="mb-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="text-warning" size={24} />
              <h2 className="text-xl font-heading font-semibold text-primary">
                Risk Flags Detected
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {riskFlags.map((flag, index) => {
                const flagData = typeof flag === 'string' 
                  ? { type: 'medium', message: flag, severity: 2 }
                  : flag;
                return (
                  <RiskFlagCard key={index} flag={flagData} />
                );
              })}
            </div>
          </div>
        )}

        {/* ROW 4: Signal Breakdown */}
        {signalBreakdown && (
          <div className="mb-6">
            <h2 className="text-xl font-heading font-semibold text-primary mb-4">
              How the Score Was Calculated
            </h2>
            <SignalBreakdown signals={signalBreakdown} />
          </div>
        )}

        {/* ROW 5: Images Submitted */}
        <div className="bg-white rounded-card border border-gray-200 p-6">
          <h2 className="text-xl font-heading font-semibold text-primary mb-4">
            Submitted Images
          </h2>
          <div className="flex gap-4 overflow-x-auto pb-2">
            {imageUrls.length > 0 ? (
              imageUrls.map((url, index) => (
                <div
                  key={index}
                  className="flex-shrink-0 w-48 h-48 bg-gray-200 rounded-input overflow-hidden cursor-pointer hover:opacity-80 transition-opacity"
                >
                  <img 
                    src={url} 
                    alt={`Store image ${index + 1}`}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.currentTarget.style.display = 'none';
                      e.currentTarget.nextElementSibling?.classList.remove('hidden');
                    }}
                  />
                  <div className="hidden w-full h-full flex items-center justify-center">
                    <p className="text-gray-500 text-sm">Image {index + 1}</p>
                  </div>
                </div>
              ))
            ) : (
              [1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className="flex-shrink-0 w-48 h-48 bg-gray-200 rounded-input flex items-center justify-center"
                >
                  <p className="text-gray-500 text-sm">Image {i}</p>
                </div>
              ))
            )}
          </div>
          <p className="text-xs text-gray-500 mt-3">Click on any image to view in full size</p>
        </div>

        {/* Assessment Metadata */}
        <div className="mt-6 bg-gray-50 rounded-card p-4 text-sm text-gray-600">
          <div className="flex items-center justify-between">
            <span>Assessment ID: <span className="font-mono font-medium">{assessment.id}</span></span>
            {assessment.assessedBy && <span>Assessed by: {assessment.assessedBy}</span>}
          </div>
        </div>
      </div>
    </PageWrapper>
  );
}
