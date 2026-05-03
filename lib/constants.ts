export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const STORE_TIERS: Record<string, {
  label: string;
  minScore: number;
  maxScore: number;
  description: string;
  color: string;
}> = {
  A: {
    label: 'Tier A — Prime Location',
    minScore: 80,
    maxScore: 100,
    description: 'Premium stores in prime locations with high footfall and excellent infrastructure',
    color: 'bg-green-100 text-green-800 border-green-300',
  },
  B: {
    label: 'Tier B — Established Store',
    minScore: 65,
    maxScore: 79,
    description: 'Well-established stores in good locations with steady customer base',
    color: 'bg-blue-100 text-blue-800 border-blue-300',
  },
  C: {
    label: 'Tier C — Growing Store',
    minScore: 50,
    maxScore: 64,
    description: 'Growing stores in developing areas with moderate footfall',
    color: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  },
  D: {
    label: 'Tier D — Small Store',
    minScore: 35,
    maxScore: 49,
    description: 'Small neighborhood stores with limited inventory and footfall',
    color: 'bg-orange-100 text-orange-800 border-orange-300',
  },
  E: {
    label: 'Tier E — Micro Store',
    minScore: 0,
    maxScore: 34,
    description: 'Micro stores in rural or low-density areas with minimal infrastructure',
    color: 'bg-gray-100 text-gray-800 border-gray-300',
  },
};

export const RISK_FLAG_DESCRIPTIONS: Record<string, string> = {
  low_inventory: 'Store has significantly lower inventory levels than expected for its tier',
  poor_organization: 'Store layout and organization need improvement for better operations',
  high_competition: 'High density of competing stores detected in the catchment area',
  low_footfall: 'Location shows lower than expected foot traffic patterns',
  inconsistent_data: 'Some data points show inconsistencies that require manual verification',
  poor_exterior: 'Store exterior condition may impact customer perception and footfall',
  limited_sku: 'Limited product variety compared to similar stores in the area',
  irregular_refill: 'Inventory refill patterns suggest irregular supply chain',
  poor_road_access: 'Limited road access may affect supply chain and customer reach',
  seasonal_dependency: 'Store shows high dependency on seasonal demand patterns',
};

export const SIGNAL_LABELS: Record<string, {
  label: string;
  hindiLabel: string;
  description: string;
  weight: number;
}> = {
  shelfDensityIndex: {
    label: 'Shelf Density',
    hindiLabel: 'शेल्फ घनत्व',
    description: 'Measures how efficiently shelf space is utilized',
    weight: 0.12,
  },
  skuDiversityScore: {
    label: 'SKU Diversity',
    hindiLabel: 'उत्पाद विविधता',
    description: 'Variety of products available in the store',
    weight: 0.10,
  },
  inventoryValueBand: {
    label: 'Inventory Value',
    hindiLabel: 'इन्वेंटरी मूल्य',
    description: 'Estimated total value of inventory in stock',
    weight: 0.15,
  },
  refillSignal: {
    label: 'Refill Frequency',
    hindiLabel: 'रीफिल आवृत्ति',
    description: 'How frequently inventory is restocked',
    weight: 0.08,
  },
  storeOrganizationScore: {
    label: 'Store Organization',
    hindiLabel: 'स्टोर संगठन',
    description: 'Overall cleanliness and organization of the store',
    weight: 0.10,
  },
  counterActivityProxy: {
    label: 'Counter Activity',
    hindiLabel: 'काउंटर गतिविधि',
    description: 'Estimated customer transaction frequency',
    weight: 0.12,
  },
  exteriorQualityScore: {
    label: 'Exterior Quality',
    hindiLabel: 'बाहरी गुणवत्ता',
    description: 'Condition and appeal of store exterior',
    weight: 0.08,
  },
  roadTypeScore: {
    label: 'Road Type',
    hindiLabel: 'सड़क प्रकार',
    description: 'Quality and type of road access',
    weight: 0.08,
  },
  catchmentDensity: {
    label: 'Catchment Density',
    hindiLabel: 'क्षेत्र घनत्व',
    description: 'Population density in the catchment area',
    weight: 0.10,
  },
  footfallProxyIndex: {
    label: 'Footfall Index',
    hindiLabel: 'फुटफॉल सूचकांक',
    description: 'Estimated foot traffic in the area',
    weight: 0.12,
  },
  competitionDensity: {
    label: 'Competition',
    hindiLabel: 'प्रतिस्पर्धा',
    description: 'Number of competing stores nearby',
    weight: 0.08,
  },
  neighbourhoodQuality: {
    label: 'Neighbourhood Quality',
    hindiLabel: 'पड़ोस गुणवत्ता',
    description: 'Overall quality and development of the area',
    weight: 0.07,
  },
};

export const RECOMMENDATION_CONFIG: Record<string, {
  label: string;
  color: string;
  bgColor: string;
  borderColor: string;
  description: string;
}> = {
  pre_approve: {
    label: 'Pre-Approved',
    color: '#10B981',
    bgColor: '#ECFDF5',
    borderColor: '#10B981',
    description: 'Store meets all criteria and is recommended for immediate approval',
  },
  needs_verification: {
    label: 'Needs Verification',
    color: '#F59E0B',
    bgColor: '#FFFBEB',
    borderColor: '#F59E0B',
    description: 'Store requires manual verification before final decision',
  },
  reject: {
    label: 'Rejected',
    color: '#EF4444',
    bgColor: '#FEF2F2',
    borderColor: '#EF4444',
    description: 'Store does not meet minimum criteria for approval',
  },
};

// Legacy exports for backward compatibility
export const TIER_LABELS: Record<string, string> = Object.fromEntries(
  Object.entries(STORE_TIERS).map(([key, value]) => [key, value.label])
);

export const TIER_COLORS: Record<string, string> = Object.fromEntries(
  Object.entries(STORE_TIERS).map(([key, value]) => [key, value.color])
);

export const RECOMMENDATION_LABELS: Record<string, string> = Object.fromEntries(
  Object.entries(RECOMMENDATION_CONFIG).map(([key, value]) => [key, value.label])
);

export const RECOMMENDATION_COLORS: Record<string, string> = Object.fromEntries(
  Object.entries(RECOMMENDATION_CONFIG).map(([key, value]) => [
    key,
    `bg-${key === 'pre_approve' ? 'success' : key === 'needs_verification' ? 'warning' : 'danger'}/10 text-${key === 'pre_approve' ? 'success' : key === 'needs_verification' ? 'warning' : 'danger'} border-${key === 'pre_approve' ? 'success' : key === 'needs_verification' ? 'warning' : 'danger'}`,
  ])
);

export const RISK_FLAG_DESCRIPTIONS_LEGACY: Record<string, string> = RISK_FLAG_DESCRIPTIONS;

export const SIGNAL_FEATURE_LABELS: Record<string, string> = Object.fromEntries(
  Object.entries(SIGNAL_LABELS).map(([key, value]) => [key, value.label])
);
