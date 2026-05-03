import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import toast from 'react-hot-toast';
import { camelizeKeys, decamelizeKeys } from 'humps';

// Check if we should use mock backend
const USE_MOCK_BACKEND = process.env.NEXT_PUBLIC_USE_MOCK === 'true' || !process.env.NEXT_PUBLIC_API_URL;

// Create axios instance
const apiClient = axios.create({
  baseURL: USE_MOCK_BACKEND ? 'http://mock-backend' : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'),
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth token and convert camelCase to snake_case
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Get token from localStorage (authStore persists there)
    const authData = localStorage.getItem('kiranalens-auth-storage');
    if (authData) {
      try {
        const { state } = JSON.parse(authData);
        const token = state?.token;
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      } catch (error) {
        console.error('Failed to parse auth data:', error);
      }
    }

    // Convert camelCase to snake_case for request data (except for FormData)
    if (config.data && !(config.data instanceof FormData)) {
      config.data = decamelizeKeys(config.data);
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors and convert snake_case to camelCase
apiClient.interceptors.response.use(
  (response) => {
    // Convert snake_case to camelCase for response data
    if (response.data && typeof response.data === 'object') {
      response.data = camelizeKeys(response.data);
      
      // Convert decimal strings to numbers for specific fields
      if (response.data.csqs && typeof response.data.csqs === 'string') {
        response.data.csqs = parseFloat(response.data.csqs);
      }
      if (response.data.confidenceScore && typeof response.data.confidenceScore === 'string') {
        response.data.confidenceScore = parseFloat(response.data.confidenceScore);
      }
      if (response.data.lat && typeof response.data.lat === 'string') {
        response.data.lat = parseFloat(response.data.lat);
      }
      if (response.data.lng && typeof response.data.lng === 'string') {
        response.data.lng = parseFloat(response.data.lng);
      }
      
      // Handle arrays of assessments
      if (response.data.items && Array.isArray(response.data.items)) {
        response.data.items = response.data.items.map((item: any) => {
          if (item.csqs && typeof item.csqs === 'string') {
            item.csqs = parseFloat(item.csqs);
          }
          if (item.confidenceScore && typeof item.confidenceScore === 'string') {
            item.confidenceScore = parseFloat(item.confidenceScore);
          }
          if (item.lat && typeof item.lat === 'string') {
            item.lat = parseFloat(item.lat);
          }
          if (item.lng && typeof item.lng === 'string') {
            item.lng = parseFloat(item.lng);
          }
          return item;
        });
      }
    }
    
    return response;
  },
  async (error: AxiosError<{ detail?: string; message?: string; errors?: any[] }>) => {
    // If using mock backend, don't show network errors
    if (USE_MOCK_BACKEND && (error.message === 'Network Error' || !error.response)) {
      // Silently fail for mock backend - the mock interceptor will handle it
      return Promise.reject(error);
    }

    const status = error.response?.status;
    const errorData = error.response?.data;
    const errorMessage = errorData?.detail || errorData?.message;

    // Handle different error types
    if (status === 401) {
      // Unauthorized - session expired
      toast.error('Session expired. Please login again.');
      
      // Clear auth state
      localStorage.removeItem('kiranalens-auth-storage');
      document.cookie = 'kiranalens-auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT';
      
      // Redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/login';
      }
    } else if (status === 422) {
      // Validation error - show specific field errors if available
      if (errorData?.errors && Array.isArray(errorData.errors)) {
        const fieldErrors = errorData.errors.map((err: any) => 
          `${err.field}: ${err.message}`
        ).join(', ');
        toast.error(`Validation error: ${fieldErrors}`);
      } else {
        toast.error(errorMessage || 'Invalid data submitted. Please check your input.');
      }
    } else if (status === 409) {
      // Conflict error (e.g., email already exists)
      toast.error(errorMessage || 'Conflict error - resource already exists.');
    } else if (status && status >= 500) {
      // Server error
      toast.error(errorMessage || 'Server error — please try again later.');
    } else if (error.code === 'ECONNABORTED') {
      // Timeout
      toast.error('Request timeout — please try again.');
    } else if (error.message === 'Network Error' || !error.response) {
      // Network error (only show if not using mock)
      if (!USE_MOCK_BACKEND) {
        toast.error('Unable to connect to server. Please check if the API is running.');
      }
    } else if (errorMessage) {
      // Other errors with message
      toast.error(errorMessage);
    }

    return Promise.reject(error);
  }
);

export default apiClient;
export { USE_MOCK_BACKEND };
