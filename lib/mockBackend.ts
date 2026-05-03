// Mock Backend - Temporary solution until real FastAPI backend is ready
// This file provides mock data that mimics the real API responses

import type { Assessment, User } from './types';

// Mock user data
export const mockUser: User = {
  id: 'USR001',
  email: 'priya.sharma@kiranalens.com',
  name: 'Priya Sharma',
  role: 'credit_officer',
  created_at: new Date().toISOString(),
};

// Mock assessments data
export const mockAssessments: Assessment[] = ([
  // Tier A - Prime Location Store in Mumbai (High Score, Pre-Approved)
  {
    id: 'ASS001',
    createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    storeName: 'Patel Provision Store',
    address: 'Shop 15, Linking Road, Bandra West, Mumbai, Maharashtra 400050',
    lat: 19.0596,
    lng: 72.8295,
    csqs: 87,
    storeTier: 'A',
    dailySalesMin: 35000,
    dailySalesMax: 55000,
    monthlyRevenueMin: 1050000,
    monthlyRevenueMax: 1650000,
    monthlyIncomeMin: 157500,
    monthlyIncomeMax: 247500,
    confidenceScore: 91,
    riskFlags: [],
    recommendation: 'pre_approve',
    status: 'complete',
    assessedBy: 'Priya Sharma',
    signalBreakdown: {
      visual: {
        shelfDensityIndex: 92,
        skuDiversityScore: 88,
        inventoryValueBand: 85,
        refillSignal: 90,
        storeOrganizationScore: 94,
        counterActivityProxy: 89,
        exteriorQualityScore: 91,
      },
      geo: {
        roadTypeScore: 95,
        catchmentDensity: 93,
        footfallProxyIndex: 91,
        competitionDensity: 78,
        neighbourhoodQuality: 96,
      },
    },
  },

  // Tier C - Average Store in Nagpur (Medium Score, Needs Verification)
  {
    id: 'ASS002',
    createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    storeName: 'Gupta Kirana Bhandar',
    address: 'Plot 42, Dharampeth, Near Gandhi Sagar Lake, Nagpur, Maharashtra 440010',
    lat: 21.1458,
    lng: 79.0882,
    csqs: 58,
    storeTier: 'C',
    dailySalesMin: 12000,
    dailySalesMax: 22000,
    monthlyRevenueMin: 360000,
    monthlyRevenueMax: 660000,
    monthlyIncomeMin: 54000,
    monthlyIncomeMax: 99000,
    confidenceScore: 67,
    riskFlags: [
      {
        type: 'medium',
        message: 'High competition in catchment area',
        severity: 2,
      },
      {
        type: 'medium',
        message: 'Irregular inventory refill patterns detected',
        severity: 2,
      },
    ],
    recommendation: 'needs_verification',
    status: 'complete',
    assessedBy: 'Priya Sharma',
    signalBreakdown: {
      visual: {
        shelfDensityIndex: 62,
        skuDiversityScore: 58,
        inventoryValueBand: 55,
        refillSignal: 48,
        storeOrganizationScore: 65,
        counterActivityProxy: 60,
        exteriorQualityScore: 63,
      },
      geo: {
        roadTypeScore: 68,
        catchmentDensity: 64,
        footfallProxyIndex: 59,
        competitionDensity: 42,
        neighbourhoodQuality: 66,
      },
    },
  },

  // Tier E - Micro Store in Rural UP (Low Score, Rejected)
  {
    id: 'ASS003',
    createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    storeName: 'Yadav General Store',
    address: 'Village Rampur, Post Tikri, Tehsil Sadar, Gorakhpur, Uttar Pradesh 273001',
    lat: 26.7606,
    lng: 83.3732,
    csqs: 28,
    storeTier: 'E',
    dailySalesMin: 2500,
    dailySalesMax: 5500,
    monthlyRevenueMin: 75000,
    monthlyRevenueMax: 165000,
    monthlyIncomeMin: 11250,
    monthlyIncomeMax: 24750,
    confidenceScore: 48,
    riskFlags: [
      {
        type: 'high',
        message: 'Significantly low inventory levels for operational viability',
        severity: 4,
      },
      {
        type: 'high',
        message: 'Poor store exterior condition affecting customer perception',
        severity: 3,
      },
      {
        type: 'medium',
        message: 'Limited SKU diversity compared to area requirements',
        severity: 2,
      },
    ],
    recommendation: 'reject',
    status: 'complete',
    assessedBy: 'Priya Sharma',
    signalBreakdown: {
      visual: {
        shelfDensityIndex: 32,
        skuDiversityScore: 28,
        inventoryValueBand: 25,
        refillSignal: 30,
        storeOrganizationScore: 35,
        counterActivityProxy: 22,
        exteriorQualityScore: 26,
      },
      geo: {
        roadTypeScore: 38,
        catchmentDensity: 24,
        footfallProxyIndex: 28,
        competitionDensity: 45,
        neighbourhoodQuality: 32,
      },
    },
  },
] as any);

// Helper to generate new assessment ID
let assessmentCounter = 4;
export function generateAssessmentId(): string {
  return `ASS${String(assessmentCounter++).padStart(3, '0')}`;
}

// Helper to create a new assessment from form data
export function createMockAssessment(data: {
  storeName?: string;
  lat: number;
  lng: number;
  notes?: string;
  imageUrls?: string[];
}): Assessment {
  const id = generateAssessmentId();
  
  // Generate random scores for demo
  const csqs = Math.floor(Math.random() * 40) + 50; // 50-90
  const tier = csqs >= 80 ? 'A' : csqs >= 65 ? 'B' : csqs >= 50 ? 'C' : 'D';
  const recommendation = csqs >= 75 ? 'pre_approve' : csqs >= 50 ? 'needs_verification' : 'reject';
  
  return {
    id,
    createdAt: new Date().toISOString(),
    storeName: data.storeName || 'New Store',
    address: `Location at ${data.lat.toFixed(4)}, ${data.lng.toFixed(4)}`,
    lat: data.lat,
    lng: data.lng,
    csqs,
    storeTier: tier,
    dailySalesMin: Math.floor(Math.random() * 20000) + 5000,
    dailySalesMax: Math.floor(Math.random() * 30000) + 25000,
    monthlyRevenueMin: Math.floor(Math.random() * 500000) + 150000,
    monthlyRevenueMax: Math.floor(Math.random() * 800000) + 700000,
    monthlyIncomeMin: Math.floor(Math.random() * 50000) + 20000,
    monthlyIncomeMax: Math.floor(Math.random() * 100000) + 100000,
    confidenceScore: Math.floor(Math.random() * 30) + 60,
    riskFlags: [],
    recommendation,
    status: 'processing',
    assessedBy: mockUser.name,
    imageUrls: data.imageUrls && data.imageUrls.length > 0 ? data.imageUrls : [
      'https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=800&q=80',
      'https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=800&q=80',
      'https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&q=80',
      'https://images.unsplash.com/photo-1534723452862-4c874018d66d?w=800&q=80'
    ],
    signalBreakdown: {
      visual: {
        shelfDensityIndex: Math.floor(Math.random() * 40) + 50,
        skuDiversityScore: Math.floor(Math.random() * 40) + 50,
        inventoryValueBand: Math.floor(Math.random() * 40) + 50,
        refillSignal: Math.floor(Math.random() * 40) + 50,
        storeOrganizationScore: Math.floor(Math.random() * 40) + 50,
        counterActivityProxy: Math.floor(Math.random() * 40) + 50,
        exteriorQualityScore: Math.floor(Math.random() * 40) + 50,
      },
      geo: {
        roadTypeScore: Math.floor(Math.random() * 40) + 50,
        catchmentDensity: Math.floor(Math.random() * 40) + 50,
        footfallProxyIndex: Math.floor(Math.random() * 40) + 50,
        competitionDensity: Math.floor(Math.random() * 40) + 50,
        neighbourhoodQuality: Math.floor(Math.random() * 40) + 50,
      },
    },
  } as any;
}
