# Quick Testing Guide - What You Can Test Now

## ✅ Features You Can Test RIGHT NOW (No Setup Needed)

### 1. Authentication & User Management
- ✅ **Login**: Use `demo@kiranalens.com` / `Demo@1234`
- ✅ **Logout**: Click logout button
- ✅ **Session management**: Token stored in localStorage and cookies
- ✅ **Protected routes**: Try accessing `/dashboard` without login

**How to test:**
1. Go to `http://localhost:3001/auth/login`
2. Enter demo credentials
3. Should redirect to dashboard
4. Logout and verify redirect to login

---

### 2. Dashboard & Data Viewing
- ✅ **View 6 demo assessments** (3 from seed + 3 duplicates)
- ✅ **Statistics cards**: Total, Pre-approved, Needs Verification, Rejected
- ✅ **Donut chart**: Recommendation breakdown
- ✅ **Recent assessments table**: Last 5 assessments
- ✅ **Average CSQS score**: Calculated from all assessments

**How to test:**
1. Login and go to dashboard
2. Verify all statistics are displayed
3. Check that charts render correctly
4. Click "View" on any assessment

---

### 3. Assessment List & Filtering
- ✅ **View all assessments**: Table with all data
- ✅ **Filter by recommendation**: pre_approve, needs_verification, reject
- ✅ **Filter by tier**: A, B, C, D, E
- ✅ **Filter by status**: pending, processing, complete, error
- ✅ **Search by store name**: Type to filter
- ✅ **Pagination**: If more than 20 items
- ✅ **Sorting**: By date, score, etc.

**How to test:**
1. Go to "All Assessments" in sidebar
2. Try each filter dropdown
3. Use search box to find stores
4. Test pagination controls

---

### 4. Assessment Details View
- ✅ **View individual assessment**: All details displayed
- ✅ **CSQS score**: With color coding
- ✅ **Store information**: Name, address, coordinates
- ✅ **Recommendation badge**: Visual status
- ✅ **Signal breakdown**: All 12 signals with scores
- ✅ **Risk flags**: If any present
- ✅ **Revenue estimates**: Min/max ranges
- ✅ **Visual & geo features**: If available

**How to test:**
1. Click "View" on any assessment from dashboard or list
2. Verify all information displays correctly
3. Check signal breakdown chart
4. View risk flags section

---

### 5. API Endpoints (Backend Testing)
Run the test script to verify all endpoints:

```bash
cd kiranalens-api
python test_assessment_creation.py
```

**What gets tested:**
- ✅ Health check endpoint
- ✅ User login
- ✅ Get current user
- ✅ Get all assessments
- ✅ Get single assessment
- ✅ Filter by recommendation
- ✅ Filter by tier
- ✅ Pagination
- ✅ Unauthorized access handling
- ✅ Invalid token handling
- ✅ CORS headers
- ✅ Rate limiting

---

## ❌ Features That Need API Keys (Can't Test Yet)

### 1. Create New Assessment
**Why it fails:** Requires Supabase storage to upload images

**Error you'll see:** "Failed to create assessment: Invalid API key"

**What you need:**
- Supabase account (free at https://supabase.com)
- Create a storage bucket named "kirana-images"
- Get your Supabase URL and anon key
- Update `.env` file

---

### 2. AI Vision Analysis
**Why it fails:** Requires Groq/OpenAI API key for image analysis

**What you need:**
- Groq API key (free at https://console.groq.com) OR
- OpenAI API key (free $5 credit)
- Update `.env` file with your key

---

### 3. Geocoding (Optional)
**Why it might fail:** Google Maps API for address lookup

**What you need:**
- Google Maps API key (free $200/month credit) OR
- Use Nominatim (already configured, free)

---

## 🎯 Recommended Testing Flow (Without API Keys)

### Test 1: Authentication Flow (5 minutes)
1. Open `http://localhost:3001`
2. Should redirect to login
3. Try wrong password → Should show error
4. Login with correct credentials → Should redirect to dashboard
5. Logout → Should redirect to login
6. Try accessing `/dashboard` without login → Should redirect to login

### Test 2: Dashboard Viewing (5 minutes)
1. Login and view dashboard
2. Check all 4 statistics cards
3. Verify donut chart displays
4. Check recent assessments table
5. Click "View" on different assessments
6. Verify data displays correctly

### Test 3: Assessment List & Filtering (10 minutes)
1. Go to "All Assessments"
2. Test each filter:
   - Recommendation: pre_approve, needs_verification, reject
   - Tier: A, B, C, D, E
   - Status: complete
3. Use search: Type "Sharma" → Should filter
4. Clear filters → Should show all
5. Click on different assessments to view details

### Test 4: Assessment Details (5 minutes)
1. Open any assessment
2. Verify all sections display:
   - Store info
   - CSQS score with color
   - Recommendation badge
   - Signal breakdown (12 signals)
   - Risk flags
   - Revenue estimates
3. Check that charts render
4. Verify images display (if URLs are valid)

### Test 5: Navigation & UI (5 minutes)
1. Test all sidebar links
2. Verify breadcrumbs work
3. Test responsive design (resize browser)
4. Check loading states
5. Verify error messages display correctly

### Test 6: API Testing (5 minutes)
```bash
cd kiranalens-api
python test_assessment_creation.py
```
Should see mostly passing tests (except features needing API keys)

---

## 📊 Test Results Checklist

Use this to track your testing:

### Authentication
- [ ] Login with correct credentials works
- [ ] Login with wrong credentials shows error
- [ ] Logout works
- [ ] Protected routes redirect to login
- [ ] Session persists on page refresh

### Dashboard
- [ ] Statistics cards show correct numbers
- [ ] Donut chart renders
- [ ] Recent assessments table displays
- [ ] Average CSQS score calculated
- [ ] "View" buttons work

### Assessment List
- [ ] All assessments display in table
- [ ] Filter by recommendation works
- [ ] Filter by tier works
- [ ] Search by store name works
- [ ] Pagination works (if applicable)
- [ ] Sorting works

### Assessment Details
- [ ] Store information displays
- [ ] CSQS score shows with correct color
- [ ] Recommendation badge displays
- [ ] Signal breakdown chart renders
- [ ] Risk flags display (if any)
- [ ] Revenue estimates show
- [ ] Back button works

### UI/UX
- [ ] Navigation works smoothly
- [ ] Loading states display
- [ ] Error messages show correctly
- [ ] Responsive design works
- [ ] No console errors

### API
- [ ] Health check returns 200
- [ ] Login returns token
- [ ] Get assessments returns data
- [ ] Filters work correctly
- [ ] Unauthorized requests return 401

---

## 🚀 To Enable Full Testing (Create New Assessments)

If you want to test the complete assessment creation flow, you need to set up API keys:

### Step 1: Get Supabase Account (5 minutes)
1. Go to https://supabase.com
2. Sign up for free account
3. Create new project
4. Go to Storage → Create bucket → Name: "kirana-images" → Public
5. Go to Settings → API → Copy:
   - Project URL
   - anon/public key

### Step 2: Get Groq API Key (2 minutes)
1. Go to https://console.groq.com
2. Sign up for free account
3. Go to API Keys → Create new key
4. Copy the key

### Step 3: Update .env File
Edit `kiranalens-api/.env`:
```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_BUCKET=kirana-images

# AI Provider
GROQ_API_KEY=your-groq-key-here
AI_PROVIDER=groq
```

### Step 4: Restart API Server
```bash
# Stop current server (Ctrl+C)
cd kiranalens-api
python main.py
```

### Step 5: Test Assessment Creation
1. Go to "New Assessment"
2. Upload 3-5 store images
3. Capture GPS location
4. Submit
5. Watch processing
6. View results

---

## 📝 What to Report

After testing, please report:

### Working Features
- List what worked correctly
- Any features that exceeded expectations

### Issues Found
- What didn't work as expected
- Steps to reproduce
- Error messages (if any)
- Screenshots (if helpful)

### Suggestions
- UI/UX improvements
- Missing features
- Performance issues

---

## 💡 Quick Tips

1. **Use Chrome DevTools**: Press F12 to see console errors
2. **Check Network Tab**: See API requests/responses
3. **Clear Cache**: If things look broken, try Ctrl+Shift+R
4. **Check Both Servers**: Make sure both frontend and backend are running
5. **Look at Logs**: Backend logs show detailed errors

---

## ❓ Common Issues & Solutions

### Issue: "Unable to connect to server"
**Solution:** Make sure API is running on port 8000
```bash
cd kiranalens-api
python main.py
```

### Issue: "Session expired"
**Solution:** Login again with demo credentials

### Issue: Dashboard shows no data
**Solution:** Check browser console for errors, verify API is running

### Issue: Images won't upload
**Solution:** This is expected - you need Supabase API keys

### Issue: Frontend on wrong port
**Solution:** Frontend might be on port 3001 instead of 3000 (check terminal)

---

## 🎉 Summary

**You can fully test:**
- ✅ Authentication (login/logout)
- ✅ Dashboard viewing
- ✅ Assessment list & filtering
- ✅ Assessment details
- ✅ All API endpoints (except creation)
- ✅ UI/UX and navigation

**You cannot test (without API keys):**
- ❌ Creating new assessments
- ❌ Image upload
- ❌ AI vision analysis
- ❌ Reprocessing assessments

**Estimated testing time:** 30-45 minutes for full manual testing

**Ready to start?** Follow the "Recommended Testing Flow" above!
