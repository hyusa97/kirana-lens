# KiranaLens - Quick Start Guide

## Installation & Setup

### 1. Install Dependencies

```bash
npm install
```

This will install:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Lucide React (icons)
- Axios (API client)
- Utility libraries (clsx, tailwind-merge, class-variance-authority)

### 2. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Build for Production

```bash
npm run build
npm start
```

## Project Overview

KiranaLens is an AI-powered underwriting platform for Indian kirana stores (small neighborhood retail shops). It analyzes store images and location data to generate credit scores and lending recommendations.

## Key Features

### 📊 Dashboard (`/dashboard`)
- Overview statistics
- Recent assessments
- Quick actions

### ➕ New Assessment (`/assess`)
- Store information form
- GPS location capture
- Multi-image upload (drag & drop)
- Real-time validation

### 🔄 Processing Screen (`/assess/[id]/processing`)
- Animated processing indicators
- Auto-redirect to results

### 📈 Assessment Results (`/assess/[id]`)
- CSQS score gauge (0-100)
- Confidence score bar
- Financial ranges (daily sales, monthly revenue, income)
- Risk flags
- Signal breakdown (12 features)
- Location map preview
- Recommendation badge

### 📋 All Assessments (`/admin`)
- Sortable table
- Search & filter
- Pagination

### 🔐 Authentication
- Login page (`/auth/login`)
- Registration page (`/auth/register`)

## Navigation

The sidebar provides access to:
- **Dashboard**: Overview and stats
- **New Assessment**: Create new assessment
- **All Assessments**: View all assessments
- **Admin**: Admin panel (role-based)
- **Logout**: Sign out

## Mock Data

The app uses mock data from `lib/mockData.ts`:
- 3 sample assessments
- 1 mock user (Priya Sharma, Analyst)

### Sample Assessments:
1. **Sharma General Store** (Bangalore) - CSQS: 78, Pre-Approved
2. **Patel Kirana Store** (Pune) - CSQS: 62, Needs Verification
3. **Kumar Provision Store** (Chennai) - CSQS: 42, Rejected

## Design System

### Colors
```css
Primary:  #1A3A5C (deep navy)
Accent:   #F59E0B (amber)
Success:  #10B981 (green)
Warning:  #F59E0B (amber)
Danger:   #EF4444 (red)
```

### Typography
- **Headings**: Inter
- **Body**: DM Sans

### Border Radius
- **Cards**: 12px
- **Inputs**: 8px
- **Badges**: 4px

## Key Components

### ScoreGauge
Circular progress indicator for CSQS score (0-100)
```tsx
<ScoreGauge score={78} label="CSQS Score" size="lg" />
```

### RangeCard
Display financial metrics in Indian Rupees
```tsx
<RangeCard 
  title="Monthly Revenue Range"
  min={450000}
  max={750000}
  icon={TrendingUp}
/>
```

### StatusBadge
Show recommendation status
```tsx
<StatusBadge status="pre_approve" size="md" />
```

### SignalBreakdown
Expandable accordion for feature scores
```tsx
<SignalBreakdown signals={assessment.signalBreakdown} />
```

### ImageUploadZone
Drag-drop image upload
```tsx
<ImageUploadZone 
  onImagesChange={(files) => setImages(files)}
  maxFiles={10}
/>
```

### GpsCapture
Capture GPS coordinates
```tsx
<GpsCapture 
  onLocationCapture={(lat, lng) => setLocation({ lat, lng })}
/>
```

## Utility Functions

### Format Rupees
```typescript
import { formatRupees } from '@/lib/utils';
formatRupees(450000); // "₹4,50,000"
```

### Format Rupees Range
```typescript
import { formatRupeesRange } from '@/lib/utils';
formatRupeesRange(450000, 750000); // "₹4,50,000 - ₹7,50,000"
```

### Format Date
```typescript
import { formatDate } from '@/lib/utils';
formatDate('2026-04-14T10:30:00Z'); // "14 Apr, 2026"
```

### Get Score Color
```typescript
import { getScoreColor } from '@/lib/utils';
getScoreColor(78); // "text-success"
getScoreColor(55); // "text-warning"
getScoreColor(35); // "text-danger"
```

## TypeScript Types

All types are defined in `lib/types.ts`:

```typescript
import type { Assessment, User, RiskFlag } from '@/lib/types';
```

### Main Types:
- `User`: User account with role
- `Assessment`: Complete assessment data
- `VisualFeatures`: 7 visual signals from images
- `GeoFeatures`: 5 geo signals from location
- `SignalBreakdown`: Combined visual + geo features
- `RiskFlag`: Risk warning with severity
- `RecommendationType`: 'pre_approve' | 'needs_verification' | 'reject'
- `AssessmentStatus`: 'draft' | 'processing' | 'completed' | 'archived'

## Constants

All constants are in `lib/constants.ts`:

```typescript
import { 
  TIER_LABELS, 
  TIER_COLORS,
  RECOMMENDATION_LABELS,
  RECOMMENDATION_COLORS,
  SIGNAL_FEATURE_LABELS 
} from '@/lib/constants';
```

## API Integration (Placeholder)

API functions are defined in `lib/api.ts`:

```typescript
import { api } from '@/lib/api';

// Auth
await api.login(email, password);
await api.register(email, password, name);

// Assessments
await api.getAssessments();
await api.getAssessment(id);
await api.createAssessment(formData);
```

**Note**: These are currently mock implementations. Update with real endpoints.

## Folder Structure

```
app/                    # Next.js pages
components/             # React components
  ├── layout/          # Layout components
  ├── ui/              # UI components
  └── assessment/      # Assessment-specific components
lib/                    # Utilities and types
  ├── api.ts           # API client
  ├── types.ts         # TypeScript types
  ├── utils.ts         # Utility functions
  ├── constants.ts     # App constants
  └── mockData.ts      # Mock data
```

## Responsive Design

- **Desktop** (>1024px): Full sidebar, multi-column layouts
- **Tablet** (768-1024px): Collapsible sidebar, responsive grids
- **Mobile** (<768px): Hamburger menu, single-column layouts

## Development Tips

### 1. Hot Reload
Changes to files automatically reload the browser.

### 2. TypeScript
All files use TypeScript for type safety. Check types in `lib/types.ts`.

### 3. Tailwind CSS
Use Tailwind utility classes. Custom colors are defined in `tailwind.config.ts`.

### 4. Component Organization
- Layout components: `components/layout/`
- UI components: `components/ui/`
- Assessment components: `components/assessment/`

### 5. Mock Data
Edit `lib/mockData.ts` to add more sample assessments.

## Next Steps

1. **API Integration**: Replace mock functions in `lib/api.ts` with real API calls
2. **Authentication**: Implement real auth with JWT tokens
3. **Map Integration**: Add Google Maps or Mapbox for location display
4. **Image Processing**: Connect to AI backend for image analysis
5. **Real-time Updates**: Add WebSocket for processing status
6. **Export Reports**: Generate PDF reports
7. **Analytics**: Add admin dashboard with charts

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000
# Or use a different port
npm run dev -- -p 3001
```

### TypeScript Errors
```bash
# Check for type errors
npm run build
```

### Styling Issues
```bash
# Rebuild Tailwind CSS
npm run dev
```

## Support

For questions or issues:
- Email: support@kiranalens.com
- Documentation: See README.md and PROJECT_STRUCTURE.md

## License

Proprietary - All rights reserved
