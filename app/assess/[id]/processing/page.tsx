'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { Loader2, Image, MapPin, Brain, Shield, FileText, CheckCircle } from 'lucide-react';
import PageWrapper from '@/components/layout/PageWrapper';
import { useQuery } from '@tanstack/react-query';
import { assessmentApi } from '@/lib/services/api';

const PROCESSING_STEPS = [
  { id: 1, label: 'Images uploaded', icon: Image, duration: 0 },
  { id: 2, label: 'Running visual analysis', icon: Brain, duration: 3000 },
  { id: 3, label: 'Querying geo-spatial data', icon: MapPin, duration: 6000 },
  { id: 4, label: 'Computing store score', icon: Brain, duration: 9000 },
  { id: 5, label: 'Applying fraud checks', icon: Shield, duration: 12000 },
  { id: 6, label: 'Generating report', icon: FileText, duration: 15000 },
];

export default function ProcessingPage() {
  const router = useRouter();
  const params = useParams();
  const id = params.id as string;
  
  // Poll the assessment status every 3 seconds
  const { data: statusData, isLoading } = useQuery({
    queryKey: ['assessment-status', id],
    queryFn: () => assessmentApi.getAssessmentStatus(id),
    refetchInterval: 3000, // Poll every 3 seconds
    enabled: !!id,
  });
  
  const [completedSteps, setCompletedSteps] = useState<number[]>([1]);
  const [currentStep, setCurrentStep] = useState(2);
  const [timeRemaining, setTimeRemaining] = useState(30);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    // Check if assessment is complete
    if (statusData?.status === 'complete') {
      setIsComplete(true);
      setCompletedSteps([1, 2, 3, 4, 5, 6]);
      setCurrentStep(7);
      setTimeout(() => {
        router.push(`/assess/${id}`);
      }, 2000);
      return;
    }

    // Handle error status
    if (statusData?.status === 'error') {
      router.push(`/assess/${id}?error=processing_failed`);
      return;
    }

    // Countdown timer
    const countdownInterval = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(countdownInterval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    // Simulate progress steps (for visual feedback while polling)
    PROCESSING_STEPS.forEach((step) => {
      if (step.duration > 0) {
        setTimeout(() => {
          setCompletedSteps((prev) => [...prev, step.id]);
          if (step.id < PROCESSING_STEPS.length) {
            setCurrentStep(step.id + 1);
          }
        }, step.duration);
      }
    });

    return () => clearInterval(countdownInterval);
  }, [id, router, statusData, isComplete]);

  return (
    <PageWrapper>
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-card border border-gray-200 p-12">
          {/* Header */}
          <div className="text-center mb-12">
            {!isComplete ? (
              <>
                <div className="inline-flex items-center justify-center w-20 h-20 bg-accent/10 rounded-full mb-6">
                  <Loader2 size={40} className="text-accent animate-spin" />
                </div>
                <h1 className="text-3xl font-heading font-bold text-primary mb-4">
                  Processing Assessment
                </h1>
                <p className="text-gray-600 mb-2">
                  Our AI is analyzing the store images and location data
                </p>
                {statusData?.progress_step && (
                  <p className="text-sm text-accent font-medium mb-2">
                    {statusData.progress_step}
                  </p>
                )}
                <p className="text-sm text-gray-500">
                  Status: <span className="font-medium text-accent">{statusData?.status || 'processing'}</span>
                </p>
              </>
            ) : (
              <>
                <div className="inline-flex items-center justify-center w-20 h-20 bg-success/10 rounded-full mb-6">
                  <CheckCircle size={40} className="text-success" />
                </div>
                <h1 className="text-3xl font-heading font-bold text-success mb-4">
                  Analysis Complete!
                </h1>
                <p className="text-gray-600">Redirecting to results...</p>
              </>
            )}
          </div>

          {/* Processing Steps */}
          <div className="space-y-4">
            {PROCESSING_STEPS.map((step) => {
              const isCompleted = completedSteps.includes(step.id);
              const isCurrent = currentStep === step.id;
              const Icon = step.icon;

              return (
                <div
                  key={step.id}
                  className={`flex items-center gap-4 p-4 rounded-input transition-all ${
                    isCompleted
                      ? 'bg-success/10 border border-success/20'
                      : isCurrent
                      ? 'bg-accent/10 border border-accent/20'
                      : 'bg-gray-50 border border-gray-200'
                  }`}
                >
                  <div
                    className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center ${
                      isCompleted
                        ? 'bg-success text-white'
                        : isCurrent
                        ? 'bg-accent text-white'
                        : 'bg-gray-200 text-gray-400'
                    }`}
                  >
                    {isCompleted ? (
                      <CheckCircle size={24} />
                    ) : isCurrent ? (
                      <Loader2 size={24} className="animate-spin" />
                    ) : (
                      <Icon size={24} />
                    )}
                  </div>
                  <div className="flex-1">
                    <p
                      className={`font-medium ${
                        isCompleted
                          ? 'text-success'
                          : isCurrent
                          ? 'text-accent'
                          : 'text-gray-500'
                      }`}
                    >
                      {step.label}
                      {isCompleted && ' ✓'}
                      {isCurrent && '...'}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Progress Bar */}
          <div className="mt-8">
            <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
              <div
                className="h-full bg-accent transition-all duration-1000 ease-out"
                style={{
                  width: `${(completedSteps.length / PROCESSING_STEPS.length) * 100}%`,
                }}
              />
            </div>
            <p className="text-center text-sm text-gray-600 mt-2">
              {completedSteps.length} of {PROCESSING_STEPS.length} steps completed
            </p>
          </div>

          {/* Assessment ID */}
          <div className="mt-8 pt-8 border-t border-gray-200 text-center">
            <p className="text-sm text-gray-500">Assessment ID: <span className="font-mono font-medium text-gray-700">{id}</span></p>
          </div>
        </div>
      </div>
    </PageWrapper>
  );
}
