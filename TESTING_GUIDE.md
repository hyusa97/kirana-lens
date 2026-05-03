# KiranaLens Testing Guide

## Overview
This guide will help you test the complete assessment creation workflow, from image upload to viewing results.

## Prerequisites
- ✅ Backend API running on `http://localhost:8000`
- ✅ Frontend running on `http://localhost:3001`
- ✅ Logged in as demo user (`demo@kiranalens.com` / `Demo@1234`)
- ✅ Demo data seeded (3 existing assessments)

---

## Test Scenario 1: View Existing Assessments

### Dashboard Testing
1. **Navigate to Dashboard** (`http://localhost:3001/dashboard`)
   - ✅ Should see 3 demo assessments
   - ✅ Statistics cards should show:
     - Total Assessments: 3
     - Pre-Approved: 1 (Sharma General Store)
     - Needs Verification: 1 (Gupta Kirana)
     - Rejected: 1 (Lal Dukan)
   - ✅ Donut chart should display recommendation breakdown
   - ✅ Average CSQS score should be displayed

2. **View Assessment Details**
   - Click "View" on any assessment
   - ✅ Should navigate to assessment detail page
   - ✅ Should show store information, CSQS score, recommendation
   - ✅ Should display signal breakdown chart
   - ✅ Should show risk flags (if any)

### All Assessments Page
1. **Navigate to All Assessments** (sidebar menu)
   - ✅ Should see table with all 3 assessments
   - ✅ Should be able to filter by status, tier, recommendation
   - ✅ Should be able to search by store name
   - ✅ Pagination should work (if more than 20 items)

---

## Test Scenario 2: Create New Assessment (Manual Testing)

### Step 1: Upload Images
1. **Navigate to New Assessment** (`http://localhost:3001/assess`)
2. **Prepare Test Images**
   - You need 3-5 images of a store (JPEG, PNG, or WebP)
   - Images should show:
     - Store exterior
     - Store interior
     - Product shelves
     - Counter area (optional)
   
3. **Upload Images**
   - Drag & drop images OR click to select
   - ✅ Should show image previews
   - ✅ Should validate minimum 3 images
   - ✅ Should validate maximum 5 images
   - ✅ Should validate file size (max 10MB per image)
   - ✅ Should validate file type (JPEG, PNG, WebP only)
   - ✅ Should show error if validation fails

### Step 2: Capture Location
1. **Click "Next" button**
2. **GPS Capture Options:**
   
   **Option A: Use Browser Geolocation**
   - Click "Use My Location" button
   - ✅ Browser should prompt for location permission
   - ✅ Should show loading state while fetching
   - ✅ Should display coordinates when captured
   - ✅ Should show accuracy in meters
   - ✅ Should show address (if geocoding works)
   
   **Option B: Manual Entry**
   - Enter coordinates manually:
     - Latitude: `19.1136` (Mumbai example)
     - Longitude: `72.8697`
   - ✅ Should validate coordinates are within India
   - ✅ Should show error if outside India boundaries

3. **Optional: Enter Store Name**
   - Enter a store name (e.g., "Test Store Mumbai")
   - ✅ Should accept alphanumeric characters

### Step 3: Confirmation
1. **Click "Next" button**
2. **Review Information**
   - ✅ Should show uploaded images count
   - ✅ Should show location coordinates
   - ✅ Should show store name (if provided)
   - ✅ Should show estimated processing time

3. **Submit Assessment**
   - Click "Submit Assessment" button
   - ✅ Should show upload progress bar
   - ✅ Should redirect to processing page

### Step 4: Processing Page
1. **Monitor Processing**
   - ✅ Should show progress indicator
   - ✅ Should display current processing step:
     - Step 1: Uploading images
     - Step 2: Vision analysis (AI processing)
     - Step 3: Geographic analysis
     - Step 4: Calculating CSQS score
   - ✅ Should auto-refresh every 3 seconds
   - ✅ Processing should complete in 30-60 seconds

2. **View Results**
   - ✅ Should automatically redirect to results page when complete
   - OR click "View Results" button

---

## Test Scenario 3: API Testing (Without Images)

Since you may not have store images readily available, you can test the API directly:

### Using Python Script

Create a test file `test_assessment_creation.py`:

```python
import requests
import json
from pathlib import Path

# Login first
login_response = requests.post('http://localhost:8000/api/v1/auth/login', json={
    'email': 'demo@kiranalens.com',
    'password': 'Demo@1234'
})
token = login_response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

print("✅ Logged in successfully")

# Test 1: Get all assessments
print("\n📊 Test 1: Fetching all assessments...")
response = requests.get('http://localhost:8000/api/v1/assessments', headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Found {len(data['items'])} assessments")
    print(f"   Total: {data['total']}, Page: {data['page']}, Pages: {data['pages']}")
else:
    print(f"❌ Failed: {response.status_code}")

# Test 2: Get single assessment
if data['items']:
    assessment_id = data['items'][0]['id']
    print(f"\n📋 Test 2: Fetching assessment {assessment_id}...")
    response = requests.get(f'http://localhost:8000/api/v1/assessments/{assessment_id}', headers=headers)
    if response.status_code == 200:
        assessment = response.json()
        print(f"✅ Store: {assessment['store_name']}")
        print(f"   CSQS: {assessment['csqs']}")
        print(f"   Tier: {assessment['store_tier']}")
        print(f"   Recommendation: {assessment['recommendation']}")
    else:
        print(f"❌ Failed: {response.status_code}")

# Test 3: Filter assessments
print("\n🔍 Test 3: Filtering assessments by recommendation...")
response = requests.get(
    'http://localhost:8000/api/v1/assessments',
    headers=headers,
    params={'recommendation': 'pre_approve'}
)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Found {len(data['items'])} pre-approved assessments")
else:
    print(f"❌ Failed: {response.status_code}")

# Test 4: Health check
print("\n🏥 Test 4: API Health Check...")
response = requests.get('http://localhost:8000/health')
if response.status_code == 200:
    health = response.json()
    print(f"✅ API Status: {health['status']}")
    print(f"   Database: {health['checks']['database']}")
    print(f"   Storage: {health['checks']['storage']}")
else:
    print(f"❌ Failed: {response.status_code}")

print("\n✅ All tests completed!")
```

Run the script:
```bash
cd kiranalens-api
python test_assessment_creation.py
```

---

## Test Scenario 4: Frontend Component Testing

### Test Individual Components

1. **Image Upload Component**
   - Test drag & drop functionality
   - Test file selection dialog
   - Test image preview
   - Test remove image functionality
   - Test validation messages

2. **GPS Capture Component**
   - Test "Use My Location" button
   - Test manual coordinate entry
   - Test validation for India boundaries
   - Test error handling for denied permissions

3. **Assessment Cards**
   - Test display of assessment information
   - Test status badges (pre-approved, needs verification, rejected)
   - Test score color coding
   - Test click to view details

4. **Dashboard Charts**
   - Test donut chart rendering
   - Test data updates
   - Test responsive design

---

## Test Scenario 5: Error Handling

### Test Error Cases

1. **Authentication Errors**
   - Try accessing protected routes without login
   - ✅ Should redirect to login page
   - Try with invalid credentials
   - ✅ Should show error message

2. **Validation Errors**
   - Upload less than 3 images
   - ✅ Should show "Minimum 3 images required"
   - Upload more than 5 images
   - ✅ Should show "Maximum 5 images allowed"
   - Upload file larger than 10MB
   - ✅ Should show size error
   - Upload non-image file
   - ✅ Should show file type error
   - Enter coordinates outside India
   - ✅ Should show boundary error

3. **Network Errors**
   - Stop the API server
   - Try to fetch assessments
   - ✅ Should show "Unable to connect to server" error
   - ✅ Should show retry button

---

## Test Scenario 6: Mock Assessment Creation

Since you need actual store images, here's how to create a mock assessment for testing:

### Option 1: Use Sample Images

1. **Download sample store images** from:
   - Google Images (search "kirana store india")
   - Unsplash (search "grocery store")
   - Or use any 3-5 images of a retail store

2. **Follow the New Assessment workflow** (Steps 1-4 above)

### Option 2: Test with Existing Demo Data

1. **View existing assessments** in the dashboard
2. **Test all viewing features**:
   - Click on each assessment
   - View detailed information
   - Check signal breakdown
   - View risk flags
   - Test filtering and sorting

---

## Expected Results Summary

### ✅ What Should Work:
1. Login/Logout functionality
2. Dashboard displays 3 demo assessments
3. View individual assessment details
4. Filter and search assessments
5. Navigate between pages
6. Responsive design on different screen sizes
7. Error messages display correctly
8. Loading states show during API calls

### ⚠️ What Won't Work (Without Valid API Keys):
1. **Creating new assessments** - Requires:
   - Valid Supabase storage key (for image upload)
   - Valid Groq/OpenAI API key (for vision analysis)
   - Valid Google Maps API key (for geocoding)

2. **Reprocessing assessments** - Same requirements as above

### 🔧 To Enable Full Functionality:

Update `.env` file in `kiranalens-api/`:
```env
# Get free Supabase account at https://supabase.com
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_BUCKET=kirana-images

# Get free Groq API key at https://console.groq.com
GROQ_API_KEY=your_groq_api_key

# Optional: Google Maps API (or use Nominatim)
GOOGLE_MAPS_API_KEY=your_google_maps_key
USE_NOMINATIM=true  # Use free OpenStreetMap instead
```

---

## Quick Test Checklist

Use this checklist for quick testing:

- [ ] Login with demo credentials
- [ ] Dashboard loads with 3 assessments
- [ ] Statistics cards show correct numbers
- [ ] Charts render correctly
- [ ] Click "View" on an assessment
- [ ] Assessment details page loads
- [ ] Navigate to "All Assessments"
- [ ] Table displays all assessments
- [ ] Filter by recommendation works
- [ ] Search by store name works
- [ ] Navigate to "New Assessment"
- [ ] Image upload zone displays
- [ ] Validation messages work
- [ ] GPS capture component displays
- [ ] Logout works correctly

---

## Troubleshooting

### Issue: "Unable to connect to server"
**Solution:** Ensure API is running on `http://localhost:8000`
```bash
cd kiranalens-api
python main.py
```

### Issue: "Session expired"
**Solution:** Login again with demo credentials

### Issue: Images won't upload
**Solution:** Check Supabase configuration in `.env` file

### Issue: Processing stuck
**Solution:** Check API logs for errors, ensure AI API keys are valid

---

## Next Steps

1. **Test with the checklist above**
2. **Report any issues you find**
3. **If you want to test full assessment creation**, you'll need to:
   - Set up Supabase account (free)
   - Get Groq API key (free)
   - Update `.env` file with valid keys

Would you like me to help you set up the API keys for full testing?
