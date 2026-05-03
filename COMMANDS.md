# KiranaLens - Commands Reference

## 🚀 Getting Started

### Install Dependencies
```bash
npm install
```

### Start Development Server
```bash
npm run dev
```
Then open [http://localhost:3000](http://localhost:3000)

### Build for Production
```bash
npm run build
```

### Start Production Server
```bash
npm start
```

### Run Linter
```bash
npm run lint
```

## 📁 Project Files Created

### Total: 38 files

#### Configuration (7)
```
✅ package.json
✅ tsconfig.json
✅ tailwind.config.ts
✅ next.config.mjs
✅ postcss.config.mjs
✅ .eslintrc.json
✅ .gitignore
```

#### Library (5)
```
✅ lib/types.ts
✅ lib/constants.ts
✅ lib/utils.ts
✅ lib/api.ts
✅ lib/mockData.ts
```

#### Components (13)
```
✅ components/layout/Sidebar.tsx
✅ components/layout/TopBar.tsx
✅ components/layout/PageWrapper.tsx
✅ components/ui/ScoreGauge.tsx
✅ components/ui/RangeCard.tsx
✅ components/ui/ConfidenceBar.tsx
✅ components/ui/RiskFlagCard.tsx
✅ components/ui/SignalBreakdown.tsx
✅ components/ui/StatusBadge.tsx
✅ components/ui/ImageUploadZone.tsx
✅ components/ui/GpsCapture.tsx
✅ components/assessment/AssessmentTable.tsx
✅ components/assessment/AssessmentCard.tsx
```

#### Pages (9)
```
✅ app/layout.tsx
✅ app/page.tsx
✅ app/globals.css
✅ app/dashboard/page.tsx
✅ app/assess/page.tsx
✅ app/assess/[id]/page.tsx
✅ app/assess/[id]/processing/page.tsx
✅ app/admin/page.tsx
✅ app/auth/login/page.tsx
✅ app/auth/register/page.tsx
```

#### Documentation (4)
```
✅ README.md
✅ PROJECT_STRUCTURE.md
✅ QUICKSTART.md
✅ BUILD_SUMMARY.md
✅ COMMANDS.md (this file)
```

## 🌐 Routes

### Public Routes
```
/auth/login          → Login page
/auth/register       → Registration page
```

### Protected Routes
```
/                    → Redirects to /dashboard
/dashboard           → Main dashboard
/assess              → New assessment form
/assess/[id]         → Assessment results
/assess/[id]/processing → Processing screen
/admin               → All assessments table
```

## 🎨 Design Tokens

### Colors (Tailwind)
```css
bg-primary      → #1A3A5C (deep navy)
bg-accent       → #F59E0B (amber)
bg-success      → #10B981 (green)
bg-warning      → #F59E0B (amber)
bg-danger       → #EF4444 (red)
```

### Border Radius (Tailwind)
```css
rounded-card    → 12px
rounded-input   → 8px
rounded-badge   → 4px
```

### Fonts (Tailwind)
```css
font-heading    → Inter
font-body       → DM Sans
```

## 📦 Key Dependencies

### Production
```json
"react": "^18.3.1"
"react-dom": "^18.3.1"
"next": "^14.2.35"
"axios": "^1.7.2"
"lucide-react": "^0.344.0"
"clsx": "^2.1.0"
"tailwind-merge": "^2.2.1"
"class-variance-authority": "^0.7.0"
```

### Development
```json
"typescript": "^5.4.2"
"@types/node": "^20.11.24"
"@types/react": "^18.2.61"
"@types/react-dom": "^18.2.19"
"tailwindcss": "^3.4.1"
"postcss": "^8.4.35"
"autoprefixer": "^10.4.18"
"eslint": "^8.57.0"
"eslint-config-next": "^14.2.35"
```

## 🔧 Utility Functions

### Import from lib/utils.ts
```typescript
import { 
  formatRupees,        // Format number as ₹4,50,000
  formatRupeesRange,   // Format range as ₹4,50,000 - ₹7,50,000
  formatScore,         // Format score as integer
  formatDate,          // Format as "14 Apr, 2026"
  formatDateTime,      // Format with time
  getScoreColor,       // Get text color class
  getScoreBgColor,     // Get background color class
  cn                   // Merge Tailwind classes
} from '@/lib/utils';
```

### Import from lib/constants.ts
```typescript
import {
  API_BASE_URL,              // API endpoint
  TIER_LABELS,               // Store tier labels
  TIER_COLORS,               // Store tier colors
  RECOMMENDATION_LABELS,     // Recommendation labels
  RECOMMENDATION_COLORS,     // Recommendation colors
  RISK_FLAG_DESCRIPTIONS,    // Risk flag descriptions
  SIGNAL_FEATURE_LABELS      // Feature labels
} from '@/lib/constants';
```

### Import from lib/types.ts
```typescript
import type {
  User,                  // User interface
  Assessment,            // Assessment interface
  VisualFeatures,        // Visual features interface
  GeoFeatures,           // Geo features interface
  SignalBreakdown,       // Signal breakdown interface
  RiskFlag,              // Risk flag interface
  RecommendationType,    // Recommendation type
  AssessmentStatus,      // Assessment status
  AssessmentFormData     // Form data interface
} from '@/lib/types';
```

## 🧪 Mock Data

### Import from lib/mockData.ts
```typescript
import { 
  mockUser,           // Mock user (Priya Sharma)
  mockAssessments     // 3 sample assessments
} from '@/lib/mockData';
```

### Sample Assessments
```
1. Sharma General Store (Bangalore)
   - CSQS: 78
   - Tier: B
   - Recommendation: Pre-Approved

2. Patel Kirana Store (Pune)
   - CSQS: 62
   - Tier: C
   - Recommendation: Needs Verification

3. Kumar Provision Store (Chennai)
   - CSQS: 42
   - Tier: D
   - Recommendation: Rejected
```

## 🎯 Component Usage Examples

### ScoreGauge
```tsx
import ScoreGauge from '@/components/ui/ScoreGauge';

<ScoreGauge 
  score={78} 
  label="CSQS Score" 
  size="lg" 
/>
```

### RangeCard
```tsx
import RangeCard from '@/components/ui/RangeCard';
import { TrendingUp } from 'lucide-react';

<RangeCard
  title="Monthly Revenue Range"
  min={450000}
  max={750000}
  icon={TrendingUp}
  iconColor="text-accent"
/>
```

### StatusBadge
```tsx
import StatusBadge from '@/components/ui/StatusBadge';

<StatusBadge 
  status="pre_approve" 
  size="md" 
/>
```

### ImageUploadZone
```tsx
import ImageUploadZone from '@/components/ui/ImageUploadZone';

<ImageUploadZone
  onImagesChange={(files) => setImages(files)}
  maxFiles={10}
/>
```

### GpsCapture
```tsx
import GpsCapture from '@/components/ui/GpsCapture';

<GpsCapture
  onLocationCapture={(lat, lng) => {
    console.log('Location:', lat, lng);
  }}
/>
```

## 📱 Responsive Breakpoints

```css
/* Mobile */
< 768px     → Single column, hamburger menu

/* Tablet */
768px - 1024px → Collapsible sidebar, 2 columns

/* Desktop */
> 1024px    → Full sidebar, 3-4 columns
```

## 🔐 Authentication Flow (Mock)

```typescript
// Login
import { api } from '@/lib/api';

const user = await api.login('analyst@kiranalens.com', 'password');
// Returns mock user object

// Register
const user = await api.register('email', 'password', 'name');
// Returns mock user object
```

## 📊 Assessment Flow

```typescript
// Create Assessment
const formData = new FormData();
formData.append('storeName', 'Store Name');
formData.append('address', 'Store Address');
// ... add images and GPS data

const assessment = await api.createAssessment(formData);
// Returns mock assessment with random ID

// Get All Assessments
const assessments = await api.getAssessments();
// Returns mockAssessments array

// Get Single Assessment
const assessment = await api.getAssessment('ASS001');
// Returns single assessment or null
```

## 🎨 Tailwind Custom Classes

```css
/* Colors */
.text-primary       → #1A3A5C
.text-accent        → #F59E0B
.text-success       → #10B981
.text-warning       → #F59E0B
.text-danger        → #EF4444

.bg-primary         → #1A3A5C
.bg-accent          → #F59E0B
.bg-success         → #10B981
.bg-warning         → #F59E0B
.bg-danger          → #EF4444

/* Border Radius */
.rounded-card       → 12px
.rounded-input      → 8px
.rounded-badge      → 4px

/* Fonts */
.font-heading       → Inter
.font-body          → DM Sans
```

## 🚀 Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker
```dockerfile
# Create Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

```bash
# Build and run
docker build -t kiranalens .
docker run -p 3000:3000 kiranalens
```

## 📝 Environment Variables

Create `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:3000/api
NEXT_PUBLIC_MAPS_API_KEY=your_maps_api_key
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000

# Or use different port
npm run dev -- -p 3001
```

### Clear Next.js Cache
```bash
rm -rf .next
npm run dev
```

### TypeScript Errors
```bash
# Check types
npx tsc --noEmit
```

### Tailwind Not Working
```bash
# Restart dev server
# Ctrl+C then npm run dev
```

## 📚 Documentation Files

```
README.md              → Main documentation
PROJECT_STRUCTURE.md   → Folder structure details
QUICKSTART.md          → Quick start guide
BUILD_SUMMARY.md       → Build summary and checklist
COMMANDS.md            → This file
```

## ✅ Quick Checklist

- [ ] Run `npm install`
- [ ] Run `npm run dev`
- [ ] Open http://localhost:3000
- [ ] Navigate to /dashboard
- [ ] Try creating new assessment
- [ ] View assessment results
- [ ] Check responsive design
- [ ] Review mock data
- [ ] Read documentation

## 🎉 You're Ready!

The project is fully set up and ready to run. Start with:

```bash
npm install
npm run dev
```

Then visit http://localhost:3000 to see KiranaLens in action!
