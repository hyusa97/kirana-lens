# KiranaLens - Complete Project Structure

```
KiranaLens/
│
├── app/                                    # Next.js 14 App Router
│   ├── layout.tsx                          # Root layout with sidebar navigation
│   ├── page.tsx                            # Home page (redirects to /dashboard)
│   ├── globals.css                         # Global styles with Tailwind
│   │
│   ├── dashboard/
│   │   └── page.tsx                        # Main dashboard with stats & recent assessments
│   │
│   ├── assess/
│   │   ├── page.tsx                        # New assessment form (upload images + GPS)
│   │   └── [id]/
│   │       ├── page.tsx                    # Assessment results view
│   │       └── processing/
│   │           └── page.tsx                # Processing screen with progress
│   │
│   ├── admin/
│   │   └── page.tsx                        # All assessments table view
│   │
│   └── auth/
│       ├── login/
│       │   └── page.tsx                    # Login page
│       └── register/
│           └── page.tsx                    # Registration page
│
├── components/                             # React components
│   ├── layout/
│   │   ├── Sidebar.tsx                     # Collapsible sidebar with navigation
│   │   ├── TopBar.tsx                      # Top header with breadcrumbs & user info
│   │   └── PageWrapper.tsx                 # Page container with padding
│   │
│   ├── ui/
│   │   ├── ScoreGauge.tsx                  # Circular 0-100 score display
│   │   ├── RangeCard.tsx                   # ₹ range metric card
│   │   ├── ConfidenceBar.tsx               # Horizontal confidence indicator
│   │   ├── RiskFlagCard.tsx                # Warning card for fraud flags
│   │   ├── SignalBreakdown.tsx             # Accordion of 12 feature scores
│   │   ├── StatusBadge.tsx                 # pre_approve/needs_verification/reject badge
│   │   ├── ImageUploadZone.tsx             # Drag-drop multi-image upload
│   │   └── GpsCapture.tsx                  # GPS button + map preview
│   │
│   └── assessment/
│       ├── AssessmentTable.tsx             # Sortable results table
│       └── AssessmentCard.tsx              # Summary card for lists
│
├── lib/                                    # Utilities and helpers
│   ├── api.ts                              # Axios client (placeholder)
│   ├── types.ts                            # All TypeScript interfaces
│   ├── utils.ts                            # formatRupees, formatScore, etc.
│   ├── constants.ts                        # API base URL, tier labels, flag descriptions
│   └── mockData.ts                         # Mock assessment data for development
│
├── .gitignore                              # Git ignore file
├── .eslintrc.json                          # ESLint configuration
├── next.config.mjs                         # Next.js configuration
├── package.json                            # Dependencies and scripts
├── postcss.config.mjs                      # PostCSS configuration
├── tailwind.config.ts                      # Tailwind CSS configuration
├── tsconfig.json                           # TypeScript configuration
├── README.md                               # Project documentation
└── PROJECT_STRUCTURE.md                    # This file
```

## Key Files Explained

### App Router Pages

| File | Purpose |
|------|---------|
| `app/layout.tsx` | Root layout with sidebar, topbar, and main content area |
| `app/page.tsx` | Home page that redirects to /dashboard |
| `app/dashboard/page.tsx` | Dashboard with stats cards and recent assessments |
| `app/assess/page.tsx` | Form to create new assessment (images + GPS) |
| `app/assess/[id]/page.tsx` | Detailed assessment results view |
| `app/assess/[id]/processing/page.tsx` | Processing animation screen |
| `app/admin/page.tsx` | Table view of all assessments with filters |
| `app/auth/login/page.tsx` | Login form |
| `app/auth/register/page.tsx` | Registration form |

### Layout Components

| Component | Purpose |
|-----------|---------|
| `Sidebar.tsx` | Left navigation with logo, menu items, and logout |
| `TopBar.tsx` | Top header with breadcrumbs and user avatar |
| `PageWrapper.tsx` | Consistent page container with title and padding |

### UI Components

| Component | Purpose |
|-----------|---------|
| `ScoreGauge.tsx` | Circular progress showing CSQS score (0-100) |
| `RangeCard.tsx` | Card displaying min-max financial ranges in ₹ |
| `ConfidenceBar.tsx` | Horizontal bar showing confidence percentage |
| `RiskFlagCard.tsx` | Alert card for risk flags with severity |
| `SignalBreakdown.tsx` | Expandable accordion for visual + geo features |
| `StatusBadge.tsx` | Colored badge for recommendation status |
| `ImageUploadZone.tsx` | Drag-drop zone for multiple image uploads |
| `GpsCapture.tsx` | Button to capture GPS coordinates |

### Assessment Components

| Component | Purpose |
|-----------|---------|
| `AssessmentTable.tsx` | Sortable table with all assessments |
| `AssessmentCard.tsx` | Card view for individual assessment summary |

### Library Files

| File | Purpose |
|------|---------|
| `lib/api.ts` | API client functions (currently placeholders) |
| `lib/types.ts` | TypeScript interfaces for Assessment, User, etc. |
| `lib/utils.ts` | Utility functions for formatting rupees, dates, scores |
| `lib/constants.ts` | App constants like tier labels, colors, descriptions |
| `lib/mockData.ts` | Mock assessment data for development |

## TypeScript Interfaces

### Main Types (from `lib/types.ts`)

```typescript
// User with role-based access
User { id, email, name, role: 'admin' | 'analyst' | 'viewer' }

// Complete assessment data
Assessment {
  id, createdAt, storeName, address, lat, lng,
  csqs, storeTier: 'A' | 'B' | 'C' | 'D',
  dailySalesMin, dailySalesMax,
  monthlyRevenueMin, monthlyRevenueMax,
  monthlyIncomeMin, monthlyIncomeMax,
  confidenceScore, riskFlags,
  recommendation: 'pre_approve' | 'needs_verification' | 'reject',
  status: 'draft' | 'processing' | 'completed' | 'archived',
  signalBreakdown: { visual, geo }
}

// Visual features from store images
VisualFeatures {
  shelfDensityIndex, skuDiversityScore, inventoryValueBand,
  refillSignal, storeOrganizationScore, counterActivityProxy,
  exteriorQualityScore
}

// Geo features from location data
GeoFeatures {
  roadTypeScore, catchmentDensity, footfallProxyIndex,
  competitionDensity, neighbourhoodQuality
}

// Risk flag with severity
RiskFlag {
  type: 'high' | 'medium' | 'low',
  message: string,
  severity: number (1-5)
}
```

## Navigation Structure

```
KiranaLens (Logo)
├── Dashboard (/)
├── New Assessment (/assess)
├── All Assessments (/admin)
├── Admin (/admin) [admin only]
└── Logout
```

## Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary | #1A3A5C | Headings, sidebar, main brand color |
| Accent | #F59E0B | Buttons, highlights, CTAs |
| Success | #10B981 | High scores, pre-approved status |
| Warning | #F59E0B | Medium scores, needs verification |
| Danger | #EF4444 | Low scores, rejected status |

## Border Radius System

| Element | Radius | Usage |
|---------|--------|-------|
| Cards | 12px | Main content cards |
| Inputs | 8px | Form inputs, buttons |
| Badges | 4px | Status badges, tags |

## Responsive Breakpoints

- **Mobile**: < 768px (single column, hamburger menu)
- **Tablet**: 768px - 1024px (collapsible sidebar)
- **Desktop**: > 1024px (full sidebar, multi-column layouts)
