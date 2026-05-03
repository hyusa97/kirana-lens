import axios from 'axios';
import { API_BASE_URL } from './constants';
import { mockAssessments, mockUser } from './mockData';
import type { Assessment, User } from './types';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Placeholder API functions - to be implemented with real endpoints
export const api = {
  // Auth
  login: async (email: string, password: string): Promise<User> => {
    // Mock implementation
    await new Promise((resolve) => setTimeout(resolve, 500));
    return mockUser;
  },

  register: async (email: string, password: string, name: string): Promise<User> => {
    // Mock implementation
    await new Promise((resolve) => setTimeout(resolve, 500));
    return {
      ...mockUser,
      email,
      name,
    };
  },

  // Assessments
  getAssessments: async (): Promise<Assessment[]> => {
    // Mock implementation - returns mock assessments
    await new Promise((resolve) => setTimeout(resolve, 300));
    return mockAssessments;
  },

  getAssessment: async (id: string): Promise<Assessment | null> => {
    // Mock implementation
    await new Promise((resolve) => setTimeout(resolve, 200));
    return mockAssessments.find((a) => a.id === id) || null;
  },

  createAssessment: async (formData: FormData): Promise<Assessment> => {
    // Mock implementation
    await new Promise((resolve) => setTimeout(resolve, 1000));
    
    const newAssessment: Assessment = {
      id: 'ASS' + Math.random().toString(36).substr(2, 6).toUpperCase(),
      createdAt: new Date().toISOString(),
      storeName: formData.get('storeName') as string,
      address: formData.get('address') as string,
      lat: parseFloat(formData.get('lat') as string) || 0,
      lng: parseFloat(formData.get('lng') as string) || 0,
      csqs: Math.floor(Math.random() * 40) + 50, // Random score 50-90
      storeTier: 'B',
      dailySalesMin: 10000,
      dailySalesMax: 20000,
      monthlyRevenueMin: 300000,
      monthlyRevenueMax: 600000,
      monthlyIncomeMin: 45000,
      monthlyIncomeMax: 90000,
      confidenceScore: Math.floor(Math.random() * 30) + 60, // Random 60-90
      riskFlags: [],
      recommendation: 'needs_verification',
      status: 'completed',
      assessedBy: mockUser.name,
      signalBreakdown: {
        visual: {
          shelfDensityIndex: Math.floor(Math.random() * 30) + 60,
          skuDiversityScore: Math.floor(Math.random() * 30) + 60,
          inventoryValueBand: Math.floor(Math.random() * 30) + 60,
          refillSignal: Math.floor(Math.random() * 30) + 60,
          storeOrganizationScore: Math.floor(Math.random() * 30) + 60,
          counterActivityProxy: Math.floor(Math.random() * 30) + 60,
          exteriorQualityScore: Math.floor(Math.random() * 30) + 60,
        },
        geo: {
          roadTypeScore: Math.floor(Math.random() * 30) + 60,
          catchmentDensity: Math.floor(Math.random() * 30) + 60,
          footfallProxyIndex: Math.floor(Math.random() * 30) + 60,
          competitionDensity: Math.floor(Math.random() * 30) + 60,
          neighbourhoodQuality: Math.floor(Math.random() * 30) + 60,
        },
      },
    };
    
    return newAssessment;
  },

  updateAssessment: async (id: string, updates: Partial<Assessment>): Promise<Assessment> => {
    // Mock implementation
    await new Promise((resolve) => setTimeout(resolve, 300));
    const assessment = mockAssessments.find((a) => a.id === id);
    if (!assessment) throw new Error('Assessment not found');
    return { ...assessment, ...updates };
  },

  deleteAssessment: async (id: string): Promise<void> => {
    // Mock implementation
    await new Promise((resolve) => setTimeout(resolve, 300));
  },
};

export default apiClient;
