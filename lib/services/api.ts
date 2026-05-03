import apiClient from '../apiClient';
import type { 
  Assessment, 
  AssessmentListResponse, 
  AssessmentStatusResponse,
  LoginRequest, 
  LoginResponse, 
  User,
  AssessmentFormData 
} from '../types';

export const authApi = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post('/api/v1/auth/login', credentials);
    return response.data;
  },

  register: async (userData: {
    name: string;
    email: string;
    password: string;
    organisation?: string;
    role?: string;
  }): Promise<User> => {
    const response = await apiClient.post('/api/v1/auth/register', userData);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/api/v1/auth/me');
    return response.data;
  },

  refreshToken: async (refreshToken: string): Promise<{ access_token: string }> => {
    const response = await apiClient.post('/api/v1/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/api/v1/auth/logout');
  },
};

export const assessmentApi = {
  getAssessments: async (params?: {
    page?: number;
    limit?: number;
    statusFilter?: string;
    storeTier?: string;
    recommendation?: string;
  }): Promise<AssessmentListResponse> => {
    const response = await apiClient.get('/api/v1/assessments', { params });
    return response.data;
  },

  getAssessment: async (id: string): Promise<Assessment> => {
    const response = await apiClient.get(`/api/v1/assessments/${id}`);
    return response.data;
  },

  getAssessmentStatus: async (id: string): Promise<AssessmentStatusResponse> => {
    const response = await apiClient.get(`/api/v1/assessments/${id}/status`);
    return response.data;
  },

  createAssessment: async (formData: FormData): Promise<Assessment> => {
    const response = await apiClient.post('/api/v1/assessments', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  reprocessAssessment: async (id: string): Promise<Assessment> => {
    const response = await apiClient.post(`/api/v1/assessments/${id}/reprocess`);
    return response.data;
  },

  deleteAssessment: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/v1/assessments/${id}`);
  },
};

export const healthApi = {
  checkHealth: async (): Promise<{
    status: string;
    timestamp: string;
    version: string;
    db_connected: boolean;
    checks: Record<string, string>;
  }> => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

// Legacy API object for backward compatibility
export const api = {
  // Auth
  login: async (email: string, password: string): Promise<User> => {
    const response = await authApi.login({ email, password });
    return response.user;
  },

  register: async (email: string, password: string, name: string): Promise<User> => {
    return await authApi.register({ name, email, password });
  },

  // Assessments
  getAssessments: async (): Promise<Assessment[]> => {
    const response = await assessmentApi.getAssessments();
    return response.items;
  },

  getAssessment: async (id: string): Promise<Assessment | null> => {
    try {
      return await assessmentApi.getAssessment(id);
    } catch (error) {
      return null;
    }
  },

  createAssessment: async (formData: FormData): Promise<Assessment> => {
    return await assessmentApi.createAssessment(formData);
  },

  updateAssessment: async (id: string, updates: Partial<Assessment>): Promise<Assessment> => {
    // Not implemented in backend yet
    throw new Error('Update assessment not implemented');
  },

  deleteAssessment: async (id: string): Promise<void> => {
    await assessmentApi.deleteAssessment(id);
  },
};