import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Format number as Indian Rupees with proper formatting
export function formatRupees(amount: number): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount);
}

// Format rupee range with en-dash
export function formatRupeeRange(min: number, max: number): string {
  const minFormatted = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(min);
  
  const maxFormatted = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(max);
  
  return `${minFormatted} – ${maxFormatted}`;
}

// Format score with one decimal place
export function formatScore(score: number): string {
  return score.toFixed(1);
}

// Get hex color based on score
export function getScoreColor(score: number): string {
  if (score > 70) return '#10B981'; // Green
  if (score >= 40) return '#F59E0B'; // Amber
  return '#EF4444'; // Red
}

// Get confidence label based on score
export function getConfidenceLabel(score: number): 'High' | 'Medium' | 'Low' {
  if (score <= 1) {
    score = score * 100;
  }
  if (score >= 75) return 'High';
  if (score >= 50) return 'Medium';
  return 'Low';
}

// Get tier label with description
export function getTierLabel(tier: string): string {
  const tierLabels: Record<string, string> = {
    A: 'Tier A — Prime Location',
    B: 'Tier B — Established Store',
    C: 'Tier C — Growing Store',
    D: 'Tier D — Small Store',
    E: 'Tier E — Micro Store',
  };
  return tierLabels[tier] || `Tier ${tier}`;
}

// Get recommendation configuration
export function getRecommendationConfig(recommendation: string): {
  label: string;
  color: string;
  bgColor: string;
  icon: any;
} {
  const configs: Record<string, any> = {
    pre_approve: {
      label: 'Pre-Approved',
      color: '#10B981',
      bgColor: '#ECFDF5',
      icon: CheckCircle,
    },
    needs_verification: {
      label: 'Needs Verification',
      color: '#F59E0B',
      bgColor: '#FFFBEB',
      icon: AlertTriangle,
    },
    reject: {
      label: 'Rejected',
      color: '#EF4444',
      bgColor: '#FEF2F2',
      icon: XCircle,
    },
  };
  return configs[recommendation] || configs.needs_verification;
}

// Get human-readable flag description
export function getFlagDescription(flag: string): string {
  const descriptions: Record<string, string> = {
    low_inventory: 'Store has significantly lower inventory levels than expected for its tier',
    poor_organization: 'Store layout and organization need improvement for better operations',
    high_competition: 'High density of competing stores detected in the catchment area',
    low_footfall: 'Location shows lower than expected foot traffic patterns',
    inconsistent_data: 'Some data points show inconsistencies that require manual verification',
    poor_exterior: 'Store exterior condition may impact customer perception and footfall',
    limited_sku: 'Limited product variety compared to similar stores in the area',
    irregular_refill: 'Inventory refill patterns suggest irregular supply chain',
  };
  return descriptions[flag] || flag.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
}

// Format relative time
export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  if (diffInSeconds < 60) return 'just now';
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
  if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 604800)} weeks ago`;
  
  return new Date(dateString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function formatDateTime(dateString: string): string {
  return new Date(dateString).toLocaleString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// Legacy functions for backward compatibility
export function formatRupeesRange(min: number, max: number): string {
  return formatRupeeRange(min, max);
}

export function getScoreBgColor(score: number): string {
  if (score >= 75) return 'bg-success';
  if (score >= 50) return 'bg-warning';
  return 'bg-danger';
}
