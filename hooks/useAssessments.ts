import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import assessmentService, { CreateAssessmentRequest, GetAssessmentsParams } from '@/lib/services/assessmentService';
import type { Assessment } from '@/lib/types';

export function useGetAssessments(params?: GetAssessmentsParams) {
  return useQuery({
    queryKey: ['assessments', params],
    queryFn: async () => {
      const response = await assessmentService.getAssessments(params);
      return response.assessments;
    },
    refetchInterval: 30000, // Refetch every 30 seconds
    staleTime: 30000,
  });
}

export function useGetAssessment(id: string, options?: { polling?: boolean }) {
  return useQuery({
    queryKey: ['assessment', id],
    queryFn: () => assessmentService.getAssessment(id),
    enabled: !!id,
    refetchInterval: options?.polling ? 3000 : false, // Poll every 3s if enabled
    staleTime: options?.polling ? 0 : 30000,
  });
}

export function useCreateAssessment() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: (data: CreateAssessmentRequest & { onUploadProgress?: (progress: number) => void }) => {
      const { onUploadProgress, ...assessmentData } = data;
      return assessmentService.createAssessment(assessmentData, onUploadProgress);
    },
    onSuccess: (assessment) => {
      // Invalidate assessments list
      queryClient.invalidateQueries({ queryKey: ['assessments'] });
      
      // Show success message
      toast.success('Assessment submitted successfully!');
      
      // Redirect to processing page
      router.push(`/assess/${assessment.id}/processing`);
    },
    onError: (error: any) => {
      const errorMessage = error.response?.data?.detail || error.response?.data?.message || 'Failed to create assessment';
      toast.error(errorMessage);
    },
  });
}

export function useReprocessAssessment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => assessmentService.reprocess(id),
    onSuccess: (assessment) => {
      queryClient.invalidateQueries({ queryKey: ['assessments'] });
      queryClient.invalidateQueries({ queryKey: ['assessment', assessment.id] });
      toast.success('Assessment reprocessing started');
    },
    onError: (error: any) => {
      const errorMessage = error.response?.data?.detail || 'Failed to reprocess assessment';
      toast.error(errorMessage);
    },
  });
}

export function useDeleteAssessment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => assessmentService.deleteAssessment(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assessments'] });
      toast.success('Assessment deleted successfully');
    },
    onError: (error: any) => {
      const errorMessage = error.response?.data?.detail || 'Failed to delete assessment';
      toast.error(errorMessage);
    },
  });
}

export function useDownloadReport() {
  return useMutation({
    mutationFn: async (id: string) => {
      const blob = await assessmentService.downloadReport(id);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `assessment-${id}-report.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    },
    onSuccess: () => {
      toast.success('Report downloaded successfully');
    },
    onError: (error: any) => {
      const errorMessage = error.response?.data?.detail || 'Failed to download report';
      toast.error(errorMessage);
    },
  });
}
