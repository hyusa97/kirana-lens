# Backend Setup Guide

## Current Status

The frontend is now fully configured to connect to your FastAPI backend, but you're seeing a **"Network error"** because the backend isn't running yet.

---

## Quick Fix Options

### Option 1: Start Your FastAPI Backend (Recommended)

If you have a FastAPI backend ready:

```bash
# Navigate to your backend directory
cd backend

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The frontend will automatically connect once the backend is running.

---

### Option 2: Temporarily Use Mock Data

If you want to test the frontend without the backend, I can create a mock API server for you.

**Would you like me to:**
1. Create a simple mock API server using JSON Server or MSW?
2. Wait for you to set up the real FastAPI backend?
3. Update the frontend to gracefully handle the missing backend?

---

## What the Frontend Expects

The frontend is configured to make requests to: `http://localhost:8000`

### Required Endpoints

#### Authentication
```
POST /api/v1/auth/login
  Request: { email: string, password: string }
  Response: { access_token: string, token_type: string, user: {...} }

POST /api/v1/auth/register
  Request: { name, email, organization, password, role }
  Response: { message: string, user: {...} }

POST /api/v1/auth/logout
  Response: void
```

#### Assessments
```
GET /api/v1/assessments
  Query: ?page=1&limit=10&recommendation=...&tier=...&search=...
  Response: { assessments: [...], total, page, limit, pages }

POST /api/v1/assessments
  Content-Type: multipart/form-data
  Body: images[], lat, lng, store_name?, gps_accuracy?, notes?
  Response: Assessment object

GET /api/v1/assessments/{id}
  Response: Assessment object

GET /api/v1/assessments/{id}/report
  Response: PDF blob

POST /api/v1/assessments/{id}/reprocess
  Response: Assessment object

DELETE /api/v1/assessments/{id}
  Response: void
```

---

## CORS Configuration

Your FastAPI backend needs to allow requests from the frontend:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Without Backend

### Option A: Mock API Server (Quick)

I can create a simple mock server that returns fake data:

```bash
# Install json-server
npm install -g json-server

# Create mock data file
# (I can generate this for you)

# Start mock server
json-server --watch db.json --port 8000
```

### Option B: Mock Service Worker (MSW)

I can set up MSW to intercept API calls and return mock data in the browser.

---

## Current Frontend Configuration

**Environment**: `.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**API Client**: `lib/apiClient.ts`
- Timeout: 30 seconds
- Auto-adds JWT token to requests
- Handles errors globally

**Error Handling**:
- Network errors show toast: "Network error — check your connection"
- This is working correctly! It's detecting that the backend isn't available.

---

## Next Steps

### If You Have a Backend Ready:

1. **Start your FastAPI backend**:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. **Verify it's running**:
   ```bash
   curl http://localhost:8000/docs
   ```
   Should show FastAPI Swagger docs.

3. **Refresh the frontend**:
   The network error will disappear once the backend responds.

### If You Need a Mock Backend:

Let me know and I can create:
1. A simple JSON Server setup
2. Mock Service Worker (MSW) configuration
3. A minimal FastAPI backend template

---

## Troubleshooting

### "Network error" persists even with backend running

**Check:**
1. Backend is running on port 8000:
   ```bash
   curl http://localhost:8000
   ```

2. CORS is configured correctly in backend

3. `.env.local` has correct URL:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Restart Next.js after changing `.env.local`:
   ```bash
   # Stop current server (Ctrl+C)
   npm run dev
   ```

### Backend on different port

If your backend runs on a different port (e.g., 8080):

Update `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8080
```

Restart Next.js.

---

## What's Working

✅ Frontend is correctly configured  
✅ API client is set up  
✅ Error handling is working (showing network error)  
✅ All pages are ready to consume API data  

❌ Backend is not running (expected)

---

## Summary

The **"Network error"** is expected and correct behavior! It means:
- ✅ Frontend is working properly
- ✅ Error handling is working
- ❌ Backend is not available yet

**To fix**: Start your FastAPI backend on port 8000, or let me know if you'd like me to create a mock backend for testing.

---

**Need Help?**

Let me know if you want me to:
1. Create a mock API server
2. Create a minimal FastAPI backend template
3. Help troubleshoot your existing backend
4. Update the frontend to work differently
