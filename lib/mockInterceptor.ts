// Mock API Interceptor - Intercepts API calls and returns mock data
// This allows the frontend to work without a real backend

import apiClient from './apiClient';
import { mockAssessments, mockUser, createMockAssessment } from './mockBackend';
import type { Assessment } from './types';

// Storage for mock assessments (in-memory)
let assessments = [...mockAssessments];

// Mock API interceptor
export function setupMockInterceptor() {
  // Intercept requests before they're sent
  apiClient.interceptors.request.use(
    async (config) => {
      const url = config.url || '';
      const method = config.method?.toUpperCase();

      // Mock authentication endpoints
      if (url.includes('/auth/login')) {
        return Promise.reject({
          response: {
            data: {
              access_token: 'mock-jwt-token-' + Date.now(),
              token_type: 'bearer',
              user: mockUser,
            },
            status: 200,
            config,
          },
          config,
          isAxiosError: true,
        });
      }

      if (url.includes('/auth/register')) {
        return Promise.reject({
          response: {
            data: {
              message: 'User registered successfully',
              user: mockUser,
            },
            status: 200,
            config,
          },
          config,
          isAxiosError: true,
        });
      }

      if (url.includes('/auth/logout')) {
        return Promise.reject({
          response: {
            data: {},
            status: 200,
            config,
          },
          config,
          isAxiosError: true,
        });
      }

      // Mock assessment endpoints
      if (url.includes('/assessments')) {
        // GET /assessments/{id}
        if (method === 'GET' && url.match(/\/assessments\/[A-Z0-9]+$/)) {
          const id = url.split('/').pop();
          const assessment = assessments.find((a) => a.id === id);
          
          if (assessment) {
            // Simulate processing -> completed transition
            if (assessment.status === 'processing' || assessment.status === 'pending') {
              const creationTime = assessment.createdAt || (assessment as any).created_at;
              const timeSinceCreation = Date.now() - new Date(creationTime).getTime();
              if (timeSinceCreation > 15000) { // 15 seconds
                assessment.status = 'complete'; // the frontend checks for 'complete'
              }
            }

            return Promise.reject({
              response: {
                data: assessment,
                status: 200,
                config,
              },
              config,
              isAxiosError: true,
            });
          } else {
            return Promise.reject({
              response: {
                data: { detail: 'Assessment not found' },
                status: 404,
                config,
              },
              config,
              isAxiosError: true,
            });
          }
        }

        // GET /assessments/{id}/status
        if (method === 'GET' && url.match(/\/assessments\/[A-Z0-9]+\/status$/)) {
          const id = url.split('/')[url.split('/').length - 2];
          const assessment = assessments.find((a) => a.id === id);
          
          if (assessment) {
            // Simulate processing -> completed transition
            if (assessment.status === 'processing' || assessment.status === 'pending') {
              const creationTime = assessment.createdAt || (assessment as any).created_at;
              const timeSinceCreation = Date.now() - new Date(creationTime).getTime();
              if (timeSinceCreation > 15000) { // 15 seconds
                assessment.status = 'complete';
              }
            }
            
            return Promise.reject({
              response: {
                data: {
                  id: assessment.id,
                  status: assessment.status === 'completed' ? 'complete' : assessment.status,
                  progress_step: 'Running visual analysis',
                  error_message: null,
                  created_at: assessment.createdAt || (assessment as any).created_at,
                  updated_at: new Date().toISOString()
                },
                status: 200,
                config,
              },
              config,
              isAxiosError: true,
            });
          } else {
            return Promise.reject({
              response: {
                data: { detail: 'Assessment not found' },
                status: 404,
                config,
              },
              config,
              isAxiosError: true,
            });
          }
        }

        // GET /assessments (list)
        if (method === 'GET' && url.endsWith('/assessments')) {
          return Promise.reject({
            response: {
              data: {
                items: assessments.filter(a => a.status === 'completed' || a.status === 'complete'),
                total: assessments.length,
                page: 1,
                limit: 10,
                pages: 1,
              },
              status: 200,
              config,
            },
            config,
            isAxiosError: true,
          });
        }

        // POST /assessments (create)
        if (method === 'POST' && url.endsWith('/assessments')) {
          const formData = config.data as FormData;
          const lat = parseFloat(formData.get('lat') as string);
          const lng = parseFloat(formData.get('lng') as string);
          const storeName = formData.get('store_name') as string;
          const notes = formData.get('notes') as string;
          
          const images = formData.getAll('images') as File[];
          const imageUrls = images.map(file => URL.createObjectURL(file));

          const newAssessment = createMockAssessment({
            lat,
            lng,
            storeName,
            notes,
            imageUrls,
          });

          assessments.unshift(newAssessment);

          // Simulate upload progress
          if (config.onUploadProgress) {
            setTimeout(() => config.onUploadProgress?.({ loaded: 25, total: 100 } as any), 100);
            setTimeout(() => config.onUploadProgress?.({ loaded: 50, total: 100 } as any), 200);
            setTimeout(() => config.onUploadProgress?.({ loaded: 75, total: 100 } as any), 300);
            setTimeout(() => config.onUploadProgress?.({ loaded: 100, total: 100 } as any), 400);
          }

          return Promise.reject({
            response: {
              data: newAssessment,
              status: 201,
              config,
            },
            config,
            isAxiosError: true,
          });
        }

        // GET /assessments/{id}/report
        if (method === 'GET' && url.includes('/report')) {
          // Return a mock PDF blob
          const pdfContent = 'Mock PDF Report Content';
          const blob = new Blob([pdfContent], { type: 'application/pdf' });
          
          return Promise.reject({
            response: {
              data: blob,
              status: 200,
              config,
            },
            config,
            isAxiosError: true,
          });
        }

        // POST /assessments/{id}/reprocess
        if (method === 'POST' && url.includes('/reprocess')) {
          const id = url.split('/')[url.split('/').length - 2];
          const assessment = assessments.find((a) => a.id === id);
          
          if (assessment) {
            assessment.status = 'processing';
            return Promise.reject({
              response: {
                data: assessment,
                status: 200,
                config,
              },
              config,
              isAxiosError: true,
            });
          }
        }

        // DELETE /assessments/{id}
        if (method === 'DELETE' && url.match(/\/assessments\/[A-Z0-9]+$/)) {
          const id = url.split('/').pop();
          assessments = assessments.filter((a) => a.id !== id);
          
          return Promise.reject({
            response: {
              data: {},
              status: 204,
              config,
            },
            config,
            isAxiosError: true,
          });
        }
      }

      // If no mock matched, let the request proceed (will fail with network error)
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Intercept responses to handle mock data
  apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
      // If this is a mock response, return it as success
      if (error.response && error.config) {
        return Promise.resolve(error.response);
      }
      return Promise.reject(error);
    }
  );
}
