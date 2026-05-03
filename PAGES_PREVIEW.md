# KiranaLens - Pages Preview

Visual description of each page in the application.

---

## 🏠 Home Page (`/`)

**Behavior**: Automatically redirects to `/dashboard`

---

## 📊 Dashboard (`/dashboard`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│ [Sidebar]  │  Dashboard                    [User Avatar] │
│            │                                              │
│ Dashboard  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐      │
│ New Assess │  │Total │ │Pre-  │ │Needs │ │Avg   │      │
│ All Assess │  │  3   │ │Appr  │ │Review│ │Score │      │
│ Logout     │  │      │ │  1   │ │  1   │ │ 60   │      │
│            │  └──────┘ └──────┘ └──────┘ └──────┘      │
│            │                                              │
│            │  ┌────────────────────────────────────────┐ │
│            │  │ Start New Assessment                   │ │
│            │  │ Upload store images and capture GPS    │ │
│            │  │                    [+ New Assessment]  │ │
│            │  └────────────────────────────────────────┘ │
│            │                                              │
│            │  Recent Assessments              [View All] │
│            │  ┌──────┐ ┌──────┐ ┌──────┐               │
│            │  │Store │ │Store │ │Store │               │
│            │  │  1   │ │  2   │ │  3   │               │
│            │  │CSQS  │ │CSQS  │ │CSQS  │               │
│            │  │ 78   │ │ 62   │ │ 42   │               │
│            │  └──────┘ └──────┘ └──────┘               │
└─────────────────────────────────────────────────────────┘
```

### Features
- **4 Stat Cards**: Total assessments, pre-approved, needs review, average score
- **CTA Banner**: Gradient background with "Start New Assessment" button
- **Recent Assessments Grid**: 3 cards showing latest assessments
- **Each Card Shows**: Store name, address, CSQS score, confidence, revenue range, date, status badge

---

## ➕ New Assessment (`/assess`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│ [Sidebar]  │  New Assessment               [User Avatar] │
│            │  Upload store images and capture location   │
│            │                                              │
│            │  ┌────────────────────────────────────────┐ │
│            │  │ Store Information                      │ │
│            │  │ Store Name: [________________]         │ │
│            │  │ Address:    [________________]         │ │
│            │  │             [________________]         │ │
│            │  └────────────────────────────────────────┘ │
│            │                                              │
│            │  ┌────────────────────────────────────────┐ │
│            │  │ GPS Location                           │ │
│            │  │ [📍 Capture GPS Location]              │ │
│            │  │                                         │ │
│            │  │ ✓ Location Captured                    │ │
│            │  │   Lat: 12.971600                       │ │
│            │  │   Lng: 77.594600                       │ │
│            │  │   [Map Preview Placeholder]            │ │
│            │  └────────────────────────────────────────┘ │
│            │                                              │
│            │  ┌────────────────────────────────────────┐ │
│            │  │ Store Images                           │ │
│            │  │ ┌──────────────────────────────────┐   │ │
│            │  │ │     📤                           │   │ │
│            │  │ │  Drag & drop images here         │   │ │
│            │  │ │  or click to select              │   │ │
│            │  │ └──────────────────────────────────┘   │ │
│            │  │                                         │ │
│            │  │ [img] [img] [img] [img]                │ │
│            │  │ 4 of 10 images uploaded                │ │
│            │  └────────────────────────────────────────┘ │
│            │                                              │
│            │  [Generate Assessment]  [Cancel]            │
└─────────────────────────────────────────────────────────┘
```

### Features
- **Store Information**: Name and address inputs
- **GPS Capture**: Button to capture browser location with map preview
- **Image Upload**: Drag-drop zone with preview grid
- **Validation**: Form validates all required fields
- **Submit**: Generates assessment and redirects to processing

---

## 🔄 Processing (`/assess/[id]/processing`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│ [Sidebar]  │  Processing                   [User Avatar] │
│            │                                              │
│            │         ┌──────────────────────────┐        │
│            │         │                          │        │
│            │         │         ⟳                │        │
│            │         │    (spinning loader)     │        │
│            │         │                          │        │
│            │         │  Processing Assessment   │        │
│            │         │                          │        │
│            │         │  Our AI is analyzing...  │        │
│            │         │                          │        │
│            │         │  ┌────────────────────┐  │        │
│            │         │  │ 📷 Analyzing Images│  │        │
│            │         │  └────────────────────┘  │        │
│            │         │  ┌────────────────────┐  │        │
│            │         │  │ 📍 Processing GPS  │  │        │
│            │         │  └────────────────────┘  │        │
│            │         │  ┌────────────────────┐  │        │
│            │         │  │ 🧠 Generating Score│  │        │
│            │         │  └────────────────────┘  │        │
│            │         │                          │        │
│            │         │  Assessment ID: ASS001   │        │
│            │         └──────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

### Features
- **Animated Spinner**: Rotating loader icon
- **Progress Steps**: 3 cards showing processing stages
- **Auto-redirect**: Redirects to results after 5 seconds
- **Assessment ID**: Shows generated ID

---

## 📈 Assessment Results (`/assess/[id]`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│ [Sidebar]  │  ← Back  Sharma General Store [Pre-Approved]│
│            │  📍 Shop 12, MG Road, Bangalore  📅 14 Apr  │
│            │                                              │
│            │  ┌──────┐  ┌─────────────────────────────┐ │
│            │  │  ⭕  │  │ Daily Sales Range           │ │
│            │  │  78  │  │ ₹15,000 - ₹25,000          │ │
│            │  │ CSQS │  ├─────────────────────────────┤ │
│            │  │      │  │ Monthly Revenue Range       │ │
│            │  │ ████ │  │ ₹4,50,000 - ₹7,50,000      │ │
│            │  │ 82%  │  ├─────────────────────────────┤ │
│            │  │Confid│  │ Monthly Income Range        │ │
│            │  │      │  │ ₹67,500 - ₹1,12,500        │ │
│            │  │Tier B│  └─────────────────────────────┘ │
│            │  └──────┘                                   │
│            │                                              │
│            │  Signal Breakdown                            │
│            │  ┌────────────────────────────────────────┐ │
│            │  │ ▼ Visual Features (7 signals)          │ │
│            │  │   Shelf Density         85             │ │
│            │  │   SKU Diversity         78             │ │
│            │  │   Inventory Value       72             │ │
│            │  │   ...                                  │ │
│            │  └────────────────────────────────────────┘ │
│            │  ┌────────────────────────────────────────┐ │
│            │  │ ▶ Geo Features (5 signals)             │ │
│            │  └────────────────────────────────────────┘ │
│            │                                              │
│            │  Store Location                              │
│            │  ┌────────────────────────────────────────┐ │
│            │  │        [Map Preview Placeholder]       │ │
│            │  │  Lat: 12.971600, Lng: 77.594600       │ │
│            │  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Features
- **Back Button**: Navigate to all assessments
- **Header**: Store name, address, date, status badge
- **Score Gauge**: Circular CSQS score (0-100) with color coding
- **Confidence Bar**: Horizontal progress bar
- **Store Tier**: Classification badge
- **3 Range Cards**: Daily sales, monthly revenue, monthly income
- **Risk Flags**: Alert cards (if any)
- **Signal Breakdown**: Expandable accordion with 12 features
- **Location Map**: Map preview placeholder
- **Metadata**: Assessment ID and assessor name

---

## 📋 All Assessments (`/admin`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│ [Sidebar]  │  All Assessments              [User Avatar] │
│            │  View and manage all assessments            │
│            │                                              │
│            │  [Search...] [Filter ▼] [Tier ▼] [+ New]   │
│            │                                              │
│            │  ┌────────────────────────────────────────┐ │
│            │  │ Store ↕ │ Date ↕ │ CSQS ↕ │ Tier │... │ │
│            │  ├────────────────────────────────────────┤ │
│            │  │ Sharma  │ 14 Apr │  78   │  B   │👁️  │ │
│            │  │ Patel   │ 13 Apr │  62   │  C   │👁️  │ │
│            │  │ Kumar   │ 12 Apr │  42   │  D   │👁️  │ │
│            │  └────────────────────────────────────────┘ │
│            │                                              │
│            │  Showing 3 assessments                       │
│            │  [Previous] Page 1 of 1 [Next]              │
└─────────────────────────────────────────────────────────┘
```

### Features
- **Search Bar**: Search by store name or address
- **Filters**: Dropdown for recommendation and tier
- **New Button**: Create new assessment
- **Sortable Table**: Click headers to sort
- **Columns**: Store name, date, CSQS, tier, revenue, recommendation, actions
- **View Action**: Eye icon to view details
- **Pagination**: Previous/Next buttons

---

## 🔐 Login (`/auth/login`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│                                                           │
│                    ┌──────────────┐                      │
│                    │              │                      │
│                    │      KL      │                      │
│                    │  (logo box)  │                      │
│                    │              │                      │
│                    │  KiranaLens  │                      │
│                    │              │                      │
│                    │ Email:       │                      │
│                    │ [__________] │                      │
│                    │              │                      │
│                    │ Password:    │                      │
│                    │ [__________] │                      │
│                    │              │                      │
│                    │ ☐ Remember   │                      │
│                    │              │                      │
│                    │ [Sign In]    │                      │
│                    │              │                      │
│                    │ Register →   │                      │
│                    └──────────────┘                      │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Features
- **Centered Card**: White card on gradient background
- **Logo**: KL logo with brand name
- **Email Input**: Email address field
- **Password Input**: Password field
- **Remember Me**: Checkbox
- **Forgot Password**: Link
- **Sign In Button**: Submit button with loading state
- **Register Link**: Link to registration page

---

## 📝 Register (`/auth/register`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│                                                           │
│                    ┌──────────────┐                      │
│                    │              │                      │
│                    │      KL      │                      │
│                    │  (logo box)  │                      │
│                    │              │                      │
│                    │ Create Acct  │                      │
│                    │              │                      │
│                    │ Name:        │                      │
│                    │ [__________] │                      │
│                    │              │                      │
│                    │ Email:       │                      │
│                    │ [__________] │                      │
│                    │              │                      │
│                    │ Password:    │                      │
│                    │ [__________] │                      │
│                    │              │                      │
│                    │ Confirm:     │                      │
│                    │ [__________] │                      │
│                    │              │                      │
│                    │ [Create]     │                      │
│                    │              │                      │
│                    │ Login →      │                      │
│                    └──────────────┘                      │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Features
- **Centered Card**: White card on gradient background
- **Logo**: KL logo with brand name
- **Name Input**: Full name field
- **Email Input**: Email address field
- **Password Input**: Password field
- **Confirm Password**: Password confirmation field
- **Create Button**: Submit button with loading state
- **Login Link**: Link to login page

---

## 📱 Mobile View

All pages are responsive with:
- **Hamburger Menu**: Sidebar collapses to hamburger icon
- **Single Column**: Cards stack vertically
- **Touch-Friendly**: Larger tap targets
- **Optimized Layout**: Content adapts to screen size

### Mobile Dashboard
```
┌─────────────────┐
│ ☰  Dashboard  👤│
├─────────────────┤
│ ┌─────────────┐ │
│ │   Total: 3  │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │ Pre-Appr: 1 │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │   Review: 1 │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │ Avg Score:60│ │
│ └─────────────┘ │
│                 │
│ [+ New Assess]  │
│                 │
│ Recent:         │
│ ┌─────────────┐ │
│ │   Store 1   │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │   Store 2   │ │
│ └─────────────┘ │
└─────────────────┘
```

---

## 🎨 Color Coding

### CSQS Score Colors
- **75-100**: Green (Success) - High score
- **50-74**: Amber (Warning) - Medium score
- **0-49**: Red (Danger) - Low score

### Recommendation Badges
- **Pre-Approved**: Green badge with border
- **Needs Verification**: Amber badge with border
- **Rejected**: Red badge with border

### Store Tiers
- **Tier A**: Green badge - Premium Store
- **Tier B**: Blue badge - Established Store
- **Tier C**: Yellow badge - Growing Store
- **Tier D**: Gray badge - Small Store

### Risk Flags
- **High**: Red background with alert triangle icon
- **Medium**: Amber background with alert circle icon
- **Low**: Blue background with info icon

---

## 🎯 User Journey

### Complete Assessment Flow
1. **Login** → `/auth/login`
2. **Dashboard** → `/dashboard`
3. **New Assessment** → `/assess`
4. **Fill Form** → Store info, GPS, images
5. **Submit** → Click "Generate Assessment"
6. **Processing** → `/assess/[id]/processing` (5 seconds)
7. **Results** → `/assess/[id]` (auto-redirect)
8. **View Details** → Score, ranges, signals, map
9. **Back to List** → `/admin`
10. **View All** → Sortable table with filters

---

## ✨ Interactive Elements

### Hover States
- **Buttons**: Slightly darker on hover
- **Cards**: Shadow increases on hover
- **Links**: Color changes on hover
- **Table Rows**: Background changes on hover

### Loading States
- **Buttons**: Show spinner when submitting
- **Processing**: Animated spinner
- **Forms**: Disabled state while loading

### Animations
- **Score Gauge**: Circular progress animates on load
- **Confidence Bar**: Horizontal bar animates on load
- **Accordion**: Smooth expand/collapse
- **Sidebar**: Smooth slide in/out

---

This preview shows the complete visual structure of all pages in KiranaLens!
