'use client';

import PageWrapper from '@/components/layout/PageWrapper';
import AssessmentTable from '@/components/assessment/AssessmentTable';
import { useGetAssessments } from '@/hooks/useAssessments';
import { PlusCircle, Loader2 } from 'lucide-react';
import Link from 'next/link';
import { SkeletonTable } from '@/components/ui/LoadingSkeleton';

export default function AdminPage() {
  const { data: assessments = [], isLoading, error } = useGetAssessments();

  return (
    <PageWrapper
      title="All Assessments"
      description="View and manage all kirana store assessments"
    >
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <input
            type="text"
            placeholder="Search by store name or address..."
            className="px-4 py-2 border border-gray-300 rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent w-80"
          />
          <select className="px-4 py-2 border border-gray-300 rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent">
            <option value="">All Recommendations</option>
            <option value="pre_approve">Pre-Approved</option>
            <option value="needs_verification">Needs Verification</option>
            <option value="reject">Rejected</option>
          </select>
          <select className="px-4 py-2 border border-gray-300 rounded-input focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent">
            <option value="">All Tiers</option>
            <option value="A">Tier A</option>
            <option value="B">Tier B</option>
            <option value="C">Tier C</option>
            <option value="D">Tier D</option>
            <option value="E">Tier E</option>
          </select>
        </div>
        <Link
          href="/assess"
          className="bg-accent hover:bg-accent/90 text-white px-6 py-2 rounded-input font-medium flex items-center gap-2 transition-colors"
        >
          <PlusCircle size={20} />
          New Assessment
        </Link>
      </div>

      {isLoading ? (
        <SkeletonTable rows={10} />
      ) : error ? (
        <div className="bg-danger/10 border border-danger rounded-card p-6 text-center">
          <p className="text-danger">Failed to load assessments. Please try again.</p>
        </div>
      ) : assessments.length === 0 ? (
        <div className="bg-white rounded-card border border-gray-200 p-12 text-center">
          <p className="text-gray-600 mb-4">No assessments found</p>
          <Link
            href="/assess"
            className="inline-flex items-center gap-2 bg-accent hover:bg-accent/90 text-white px-6 py-3 rounded-input font-medium transition-colors"
          >
            <PlusCircle size={20} />
            Create Your First Assessment
          </Link>
        </div>
      ) : (
        <>
          <AssessmentTable assessments={assessments} />

          <div className="mt-6 flex items-center justify-between text-sm text-gray-600">
            <p>Showing {assessments.length} assessments</p>
            <div className="flex items-center gap-2">
              <button className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50">
                Previous
              </button>
              <span className="px-3 py-1">Page 1 of 1</span>
              <button className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50">
                Next
              </button>
            </div>
          </div>
        </>
      )}
    </PageWrapper>
  );
}
