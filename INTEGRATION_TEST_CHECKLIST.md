# KiranaLens Frontend-Backend Integration Test Checklist

## Prerequisites
- [ ] Backend API server running on `http://localhost:8000`
- [ ] Demo data seeded (`python kiranalens-api/scripts/seed_demo_data.py`)
- [ ] Frontend running on `http://localhost:3000`
- [ ] Environment variables configured (`.env.local`)

## Test Checklist

### 1. Authentication Flow
- [ ] **Login with demo credentials**
  - Navigate to `/auth/login`
  - Click "Demo Mode" button (bottom-left, development only)
  - Verify form fills with `demo@kiranalens.com` / `Demo@1234`
  - Submit form
  - Verify successful login and redirect to `/dashboard`
  - Check browser dev tools: JWT token stored in localStorage

- [ ] **Logout functionality**
  - Click logout button/link
  - Verify token cleared from localStorage
  - Verify redirect to `/auth/login`
  - Try accessing `/dashboard` → should redirect to login

### 2. Dashboard Integration
- [ ] **Dashboard loads real data**
  - Navigate to `/dashboard`
  - Verify 3 demo assessments visible in recent assessments table
  - Check metrics cards show correct totals:
    - Total Assessments: 3
    - Pre-Approved: 1 (Sharma General Store)
    - Needs Verification: 1 (Gupta Kirana)
    - Rejected: 1 (Lal Dukan)
  - Verify donut chart displays recommendation breakdown
  - Check average CSQS score calculation

- [ ] **Assessment data accuracy**
  - Verify Sharma General Store: CSQS ~82.1, Tier A
  - Verify Gupta Kirana: CSQS ~52.4, Tier C, has risk flags
  - Verify Lal Dukan: CSQS ~18.7, Tier E
  - Check dates, addresses, and other metadata

### 3. Assessment Detail View
- [ ] **Navigate to assessment details**
  - Click "View" on any assessment from dashboard
  - Verify URL: `/assess/[id]`
  - Verify assessment loads with complete data

- [ ] **Data display accuracy**
  - Check CSQS score and tier display correctly
  - Verify financial metrics (daily sales, monthly revenue/income)
  - Check confidence score and recommendation
  - Verify risk flags display (if any)
  - Check signal breakdown chart/data
  - Verify images section (may show placeholder if no real images)

### 4. New Assessment Creation
- [ ] **Assessment form submission**
  - Navigate to `/assess` (or click "New Assessment" button)
  - Fill out form:
    - Store name: "Test Store Integration"
    - Upload 3 test images (any JPG/PNG files)
    - Enable GPS capture or manually enter coordinates
    - Submit form

- [ ] **Form validation**
  - Try submitting without images → should show validation error
  - Try submitting with invalid coordinates → should show API validation error
  - Try submitting with too many images → should show validation error

- [ ] **Successful submission**
  - Verify successful submission redirects to `/assess/[id]/processing`
  - Check assessment created in backend (new ID generated)

### 5. Processing Page Polling
- [ ] **Processing page functionality**
  - After creating assessment, verify redirect to processing page
  - Check URL: `/assess/[id]/processing`
  - Verify page polls `/api/v1/assessments/{id}/status` every 3 seconds
  - Check browser dev tools Network tab for polling requests

- [ ] **Status updates**
  - Verify processing steps animate/update
  - Check status text updates based on API response
  - For demo data (already complete), should redirect to results quickly

- [ ] **Completion handling**
  - When status becomes 'complete', verify auto-redirect to `/assess/[id]`
  - Check error handling if status becomes 'error'

### 6. Error State Testing
- [ ] **Backend offline testing**
  - Stop the backend server (`Ctrl+C` in API terminal)
  - Refresh dashboard page
  - Verify graceful error state displays:
    - "Unable to Connect" message
    - Network error icon
    - "Try Again" button
  - Click "Try Again" → should attempt to refetch
  - Restart backend and verify recovery

- [ ] **API validation errors**
  - Try creating assessment with invalid data:
    - Coordinates outside India (lat: 0, lng: 0)
    - Invalid file types
    - Missing required fields
  - Verify API validation errors display properly
  - Check toast notifications for error messages

### 7. Loading States
- [ ] **Loading skeletons**
  - Refresh dashboard and verify loading skeletons appear
  - Check assessment detail page loading states
  - Verify form submission loading states
  - Check processing page loading indicators

### 8. Data Transformation
- [ ] **Snake_case to camelCase conversion**
  - Open browser dev tools → Network tab
  - Make API requests and check:
    - Request data uses snake_case (if applicable)
    - Response data gets converted to camelCase in frontend
  - Verify decimal fields (csqs, confidence_score) convert to numbers
  - Check date fields format properly

### 9. Navigation and Routing
- [ ] **Protected routes**
  - Without login, try accessing `/dashboard` → should redirect to login
  - Try accessing `/assess` → should redirect to login
  - Try accessing `/assess/[id]` → should redirect to login

- [ ] **Authenticated navigation**
  - After login, verify all routes accessible
  - Check breadcrumbs and navigation links work
  - Verify back buttons and internal links function

### 10. Real-time Features
- [ ] **Status polling**
  - Create new assessment
  - Verify processing page polls status every 3 seconds
  - Check Network tab for regular API calls
  - Verify polling stops after completion/error

### 11. Mobile Responsiveness
- [ ] **Mobile layout testing**
  - Open browser dev tools → Toggle device toolbar
  - Test on mobile viewport (375px width)
  - Verify responsive design works on all pages
  - Check touch interactions and mobile navigation

## Error Scenarios to Test

### Network Errors
- [ ] Slow network (throttle in dev tools)
- [ ] Intermittent connectivity
- [ ] Backend server restart during operation

### API Errors
- [ ] 401 Unauthorized (expired token)
- [ ] 422 Validation errors
- [ ] 500 Server errors
- [ ] Rate limiting (if applicable)

### Data Edge Cases
- [ ] Empty assessment list
- [ ] Assessment with missing optional fields
- [ ] Very long store names/addresses
- [ ] Special characters in input

## Performance Checks
- [ ] **Page load times**
  - Dashboard loads within 2 seconds
  - Assessment details load within 1 second
  - Form submissions respond within 3 seconds

- [ ] **API efficiency**
  - No unnecessary API calls
  - Proper caching of assessment data
  - Efficient polling intervals

## Browser Compatibility
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (if on Mac)
- [ ] Edge (latest)

## Final Integration Verification
- [ ] Complete user journey: Login → Dashboard → View Assessment → Create New → Processing → Results → Logout
- [ ] All demo data displays correctly
- [ ] All error states handle gracefully
- [ ] All loading states appear appropriately
- [ ] No console errors in browser dev tools
- [ ] API requests/responses look correct in Network tab

## Notes
- Record any issues found during testing
- Note performance observations
- Document any UX improvements needed
- Check for accessibility compliance (basic keyboard navigation)

---

**Test Environment:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Demo User: demo@kiranalens.com / Demo@1234
- Test Date: ___________
- Tester: ___________