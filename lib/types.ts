export interface User {
  id: string;
  email: string;
  name: string;
  organisation?: string;
  role: 'admin' | 'credit_officer' | 'branch_manager';
  created_at: string;
}

export interface VisualFeatures {
  id: string;
  assessment_id: string;
  shelf_density_index: number;
  sku_diversity_score: number;
  store_organization_score: number;
  counter_activity_proxy: number;
  exterior_quality_score: number;
  inventory_value_band: 'low' | 'medium' | 'high' | 'very_high';
  refill_signal: 'partially_empty' | 'normal' | 'overfilled';
  image_quality_warnings: string[];
  created_at: string;
}

export interface GeoFeatures {
  id: string;
  assessment_id: string;
  road_type_score: number;
  catchment_density_score: number;
  footfall_proxy_index: number;
  competition_density_score: number;
  neighbourhood_quality_score: number;
  competitor_count: number;
  poi_count: number;
  created_at: string;
}

export interface SignalBreakdown {
  shelf_density_index: number;
  sku_diversity_score: number;
  inventory_value_band: number;
  refill_signal: number;
  store_organization_score: number;
  counter_activity_proxy: number;
  exterior_quality_score: number;
  road_type_score: number;
  catchment_density_score: number;
  footfall_proxy_index: number;
  competition_density_score: number;
  neighbourhood_quality_score: number;
}

export type RecommendationType = 'pre_approve' | 'needs_verification' | 'reject';
export type AssessmentStatus = 'pending' | 'processing' | 'complete' | 'error';

export interface Assessment {
  id: string;
  created_at: string;
  updated_at: string;
  user_id: string;
  store_name: string | null;
  address: string | null;
  lat: string; // Decimal as string from backend
  lng: string; // Decimal as string from backend
  gps_accuracy_metres: number | null;
  image_urls: string[];
  status: AssessmentStatus;
  error_message: string | null;
  csqs: string | null; // Decimal as string from backend
  store_tier: 'A' | 'B' | 'C' | 'D' | 'E' | null;
  confidence_score: string | null; // Decimal as string from backend
  daily_sales_min: number | null;
  daily_sales_max: number | null;
  monthly_revenue_min: number | null;
  monthly_revenue_max: number | null;
  monthly_income_min: number | null;
  monthly_income_max: number | null;
  risk_flags: string[];
  recommendation: RecommendationType | null;
  signal_breakdown: SignalBreakdown | null;
  pdf_report_url: string | null;
  visual_features: VisualFeatures | null;
  geo_features: GeoFeatures | null;
}

// Frontend-friendly transformed types (after camelCase conversion)
export interface AssessmentTransformed {
  id: string;
  createdAt: string;
  updatedAt: string;
  userId: string;
  storeName: string | null;
  address: string | null;
  lat: number; // Converted to number
  lng: number; // Converted to number
  gpsAccuracyMetres: number | null;
  imageUrls: string[];
  status: AssessmentStatus;
  errorMessage: string | null;
  csqs: number | null; // Converted to number
  storeTier: 'A' | 'B' | 'C' | 'D' | 'E' | null;
  confidenceScore: number | null; // Converted to number
  dailySalesMin: number | null;
  dailySalesMax: number | null;
  monthlyRevenueMin: number | null;
  monthlyRevenueMax: number | null;
  monthlyIncomeMin: number | null;
  monthlyIncomeMax: number | null;
  riskFlags: string[];
  recommendation: RecommendationType | null;
  signalBreakdown: SignalBreakdown | null;
  pdfReportUrl: string | null;
  visualFeatures: VisualFeatures | null;
  geoFeatures: GeoFeatures | null;
}

export interface AssessmentListResponse {
  items: Assessment[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface AssessmentStatusResponse {
  id: string;
  status: AssessmentStatus;
  progress_step: string;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface AssessmentFormData {
  storeName: string;
  address: string;
  lat?: number;
  lng?: number;
  gpsAccuracyMetres?: number;
  images: File[];
}
