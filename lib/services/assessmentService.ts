import apiClient from '../apiClient';
import { assessmentApi } from './api';
import type { Assessment, AssessmentListResponse, AssessmentStatusResponse } from '../types';

export interface CreateAssessmentRequest {
  images: File[];
  lat: number;
  lng: number;
  storeName?: string;
  gpsAccuracyMetres?: number;
  monthlyRent?: number;
  yearsInOperation?: number;
  shopSize?: number;
}

export interface GetAssessmentsParams {
  page?: number;
  limit?: number;
  statusFilter?: string;
  storeTier?: string;
  recommendation?: string;
}

export interface UploadProgressCallback {
  (progress: number): void;
}

const assessmentService = {
  /**
   * Create new assessment with images and GPS data
   */
  async createAssessment(
    data: CreateAssessmentRequest,
    onUploadProgress?: UploadProgressCallback
  ): Promise<Assessment> {
    const formData = new FormData();

    // Add images
    data.images.forEach((image) => {
      formData.append('images', image);
    });

    // Add GPS data
    formData.append('lat', data.lat.toString());
    formData.append('lng', data.lng.toString());

    // Add optional fields
    if (data.storeName) {
      formData.append('store_name', data.storeName);
    }
    if (data.gpsAccuracyMetres) {
      formData.append('gps_accuracy_metres', data.gpsAccuracyMetres.toString());
    }
    if (data.monthlyRent) {
      formData.append('monthly_rent', data.monthlyRent.toString());
    }
    if (data.yearsInOperation !== undefined) {
      formData.append('years_in_operation', data.yearsInOperation.toString());
    }
    if (data.shopSize) {
      formData.append('shop_size', data.shopSize.toString());
    }

    const response = await apiClient.post<Assessment>('/api/v1/assessments', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onUploadProgress && progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onUploadProgress(percentCompleted);
        }
      },
    });

    return response.data;
  },

  /**
   * Get all assessments with optional filters
   */
  async getAssessments(params?: GetAssessmentsParams): Promise<{ assessments: Assessment[]; total: number; page: number; limit: number; pages: number }> {
    const response = await assessmentApi.getAssessments(params);
    return {
      assessments: response.items,
      total: response.total,
      page: response.page,
      limit: response.limit,
      pages: response.pages,
    };
  },

  /**
   * Get single assessment by ID
   */
  async getAssessment(id: string): Promise<Assessment> {
    return await assessmentApi.getAssessment(id);
  },

  /**
   * Get assessment status for polling
   */
  async getAssessmentStatus(id: string): Promise<AssessmentStatusResponse> {
    return await assessmentApi.getAssessmentStatus(id);
  },

  /**
   * Download assessment report as PDF
   */
  async downloadReport(id: string): Promise<Blob> {
    const response = await apiClient.get(`/api/v1/assessments/${id}/report`, {
      responseType: 'blob',
    });
    return response.data;
  },

  /**
   * Reprocess an assessment
   */
  async reprocess(id: string): Promise<Assessment> {
    return await assessmentApi.reprocessAssessment(id);
  },

  /**
   * Delete an assessment
   */
  async deleteAssessment(id: string): Promise<void> {
    await assessmentApi.deleteAssessment(id);
  },
};

export default assessmentService;
