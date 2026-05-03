# KiranaLens

An AI-powered kirana store cash flow underwriting platform for Indian NBFCs.

## Overview

KiranaLens uses computer vision and geospatial analysis to assess kirana stores (small neighborhood retail shops in India) for credit underwriting. The platform analyzes store images and location data to generate a Credit Score Quantitative Score (CSQS) and provide lending recommendations.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios (placeholder)

## Design System

### Colors
- **Primary**: #1A3A5C (deep navy)
- **Accent**: #F59E0B (amber)
- **Success**: #10B981
- **Warning**: #F59E0B
- **Danger**: #EF4444

### Typography
- **Headings**: Inter
- **Body**: DM Sans

### Border Radius
- **Cards**: 12px
- **Inputs**: 8px
- **Badges**: 4px

## Project Structure

```
├── app/
│   ├── layout.tsx                      # Root layout with sidebar
│   ├── page.tsx                        # Redirects to /dashboard
│   ├── globals.css                     # Global styles
│   ├── dashboard/page.tsx              # Main dashboard
│   ├── assess/
│   │   ├── page.tsx                    # New assessment form
│   │   └── [id]/
│   │       ├── page.tsx                # Assessment results
│   │       └── processing/page.tsx     # Processing screen
│   ├── admin/page.tsx                  # All assessments table
│   └── auth/
│       ├── login/page.tsx              # Login page
│       └── register/page.tsx           # Registration page
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx                 # Collapsible sidebar navigation
│   │   ├── TopBar.tsx                  # Top header with breadcrumbs
│   │   └── PageWrapper.tsx             # Page container
│   ├── ui/
│   │   ├── ScoreGauge.tsx              # Circular 0-100 score display
│   │   ├── RangeCard.tsx               # ₹ range metric card
│   │   ├── ConfidenceBar.tsx           # Horizontal confidence indicator
│   │   ├── RiskFlagCard.tsx            # Warning card for fraud flags
│   │   ├── SignalBreakdown.tsx         # Accordion of feature scores
│   │   ├── StatusBadge.tsx             # Recommendation badge
│   │   ├── ImageUploadZone.tsx         # Drag-drop image upload
│   │   └── GpsCapture.tsx              # GPS capture button
│   └── assessment/
│       ├── AssessmentTable.tsx         # Sortable results table
│       └── AssessmentCard.tsx          # Summary card
├── lib/
│   ├── api.ts                          # API client (placeholder)
│   ├── types.ts                        # TypeScript interfaces
│   ├── utils.ts                        # Utility functions
│   ├── constants.ts                    # App constants
│   └── mockData.ts                     # Mock assessment data
└── package.json
```

## Features

### 1. Dashboard
- Overview statistics (total assessments, pre-approved, needs review)
- Average CSQS score
- Recent assessments grid
- Quick action to start new assessment

### 2. New Assessment Flow
- Store information form (name, address)
- GPS location capture with map preview
- Multi-image upload with drag-and-drop
- Real-time validation
- Processing screen with progress indicators

### 3. Assessment Results
- CSQS score gauge (0-100)
- Confidence score bar
- Store tier classification (A/B/C/D)
- Financial ranges (daily sales, monthly revenue, monthly income)
- Risk flags with severity levels
- Signal breakdown (visual + geo features)
- Location map preview
- Recommendation badge (pre-approve/needs verification/reject)

### 4. All Assessments
- Sortable table view
- Search and filter functionality
- Quick view actions
- Pagination

### 5. Authentication
- Login page
- Registration page
- Mock authentication flow

## Key Components

### ScoreGauge
Circular progress indicator showing CSQS score (0-100) with color coding:
- Green (75-100): High score
- Amber (50-74): Medium score
- Red (0-49): Low score

### SignalBreakdown
Accordion showing 12 feature scores:
- **Visual Features** (7): Shelf density, SKU diversity, inventory value, refill signal, organization, counter activity, exterior quality
- **Geo Features** (5): Road type, catchment density, footfall index, competition, neighbourhood quality

### RangeCard
Displays financial metrics in Indian Rupees (₹) with min-max ranges

### StatusBadge
Shows recommendation status:
- **Pre-Approved**: Green badge
- **Needs Verification**: Amber badge
- **Rejected**: Red badge

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

### Build for Production

```bash
npm run build
npm start
```

## Mock Data

The application currently uses mock data defined in `lib/mockData.ts`. Three sample assessments are included with varying scores and recommendations.

## API Integration

API functions are defined in `lib/api.ts` as placeholders. To integrate with a real backend:

1. Update `API_BASE_URL` in `lib/constants.ts`
2. Implement the API functions in `lib/api.ts`
3. Add authentication token management
4. Update components to handle loading and error states

## Responsive Design

- **Desktop**: Full sidebar navigation, multi-column layouts
- **Tablet**: Collapsible sidebar, responsive grids
- **Mobile**: Hamburger menu, single-column layouts

## Future Enhancements

- Real API integration
- User authentication and authorization
- Real-time assessment processing
- Interactive map integration (Google Maps/Mapbox)
- Export reports to PDF
- Assessment history and audit trail
- Admin dashboard with analytics
- Bulk assessment upload
- Email notifications
- Role-based access control

## License

Proprietary - All rights reserved

## Support

For support, contact: support@kiranalens.com
