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
  visual?: Record<string, number | string | string[]>;
  geo?: Record<string, number | string>;
  economic_breakdown?: EconomicBreakdown;
  [key: string]: any;
}

export interface EconomicBreakdown {
  inventory_capacity?: [number, number];
  turnover_days?: [number, number];
  demand_index?: [number, number];
  competition_factor?: [number, number];
  efficiency_factor?: [number, number];
  manual_adjustment?: [number, number];
  supply_sales?: [number, number];
  demand_sales?: [number, number];
  margin_range?: [number, number];
  [key: string]: [number, number] | undefined;
}

export interface RiskFlag {
  type: 'high' | 'medium' | 'low';
  message: string;
  severity: number;
}

export type RecommendationType = 'pre_approve' | 'proceed_with_caution' | 'needs_verification' | 'reject';
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
  monthly_rent: number | null;
  years_in_operation: number | null;
  shop_size: number | null;
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
  daily_sales_range?: [number, number] | null;
  monthly_revenue_range?: [number, number] | null;
  monthly_income_range?: [number, number] | null;
  risk_flags: string[];
  recommendation: RecommendationType | null;
  signal_breakdown: SignalBreakdown | null;
  economic_breakdown?: EconomicBreakdown | null;
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
  monthlyRent: number | null;
  yearsInOperation: number | null;
  shopSize: number | null;
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
  dailySalesRange?: [number, number] | null;
  monthlyRevenueRange?: [number, number] | null;
  monthlyIncomeRange?: [number, number] | null;
  riskFlags: string[];
  recommendation: RecommendationType | null;
  signalBreakdown: SignalBreakdown | null;
  economicBreakdown?: EconomicBreakdown | null;
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
  monthlyRent?: number;
  yearsInOperation?: number;
  shopSize?: number;
  images: File[];
}
