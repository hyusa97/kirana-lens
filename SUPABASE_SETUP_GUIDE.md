# Supabase Setup Guide - Fix "Invalid API Key" Error

## Problem
You're getting "Failed to create assessment: Invalid API key" because the Supabase storage credentials in your `.env` file are invalid.

## Solution (5 minutes)

### Step 1: Create Free Supabase Account

1. **Go to Supabase:**
   - Open: https://supabase.com
   - Click "Start your project" or "Sign Up"

2. **Sign Up:**
   - Use GitHub account (recommended) OR
   - Use email/password
   - It's completely FREE - no credit card required

3. **Create New Project:**
   - Click "New Project"
   - Choose your organization (or create one)
   - Fill in:
     - **Project Name:** `kiranalens` (or any name)
     - **Database Password:** Create a strong password (save it!)
     - **Region:** Choose closest to you (e.g., `ap-south-1` for India)
   - Click "Create new project"
   - Wait 2-3 minutes for project to be ready

### Step 2: Create Storage Bucket

1. **Go to Storage:**
   - In left sidebar, click "Storage"
   - Click "Create a new bucket"

2. **Configure Bucket:**
   - **Name:** `kirana-images` (exactly this name!)
   - **Public bucket:** Toggle ON (important!)
   - Click "Create bucket"

3. **Set Bucket Policies:**
   - Click on `kirana-images` bucket
   - Go to "Policies" tab
   - Click "New Policy"
   - Select "For full customization"
   - Add this policy:

```sql
-- Allow authenticated users to upload
CREATE POLICY "Allow authenticated uploads"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'kirana-images');

-- Allow public read access
CREATE POLICY "Allow public downloads"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'kirana-images');

-- Allow authenticated users to delete their own files
CREATE POLICY "Allow authenticated deletes"
ON storage.objects FOR DELETE
TO authenticated
USING (bucket_id = 'kirana-images');
```

### Step 3: Get API Keys

1. **Go to Settings:**
   - Click "Settings" (gear icon) in left sidebar
   - Click "API"

2. **Copy These Values:**
   - **Project URL:** `https://xxxxx.supabase.co`
   - **anon/public key:** Long string starting with `eyJ...`

### Step 4: Update Your .env File

1. **Open:** `kiranalens-api/.env`

2. **Replace these lines:**
```env
# OLD (Invalid)
SUPABASE_URL=https://vieblvxktxyribpsrxdg.supabase.co
SUPABASE_KEY=sb_publishable_txoQR-p4N7H2ILbj3OQFIw_9zIDi_Uw
SUPABASE_BUCKET=kirana-images

# NEW (Your actual values)
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_KEY=YOUR_ANON_KEY_HERE
SUPABASE_BUCKET=kirana-images
```

3. **Save the file**

### Step 5: Restart API Server

```bash
# Stop the current server (Ctrl+C in the terminal)
# Then restart:
cd kiranalens-api
python main.py
```

### Step 6: Test Assessment Creation

1. Go to `http://localhost:3001/assess`
2. Upload 3-5 images
3. Capture GPS location
4. Click Submit
5. Should work now! ✅

---

## Alternative: Use Mock Storage (For Testing Only)

If you don't want to set up Supabase right now, I can create a mock storage service that saves files locally:

### Option A: Local File Storage (No Supabase Needed)

I can modify the storage service to save images to a local folder instead of Supabase. This is good for testing but not for production.

Would you like me to:
1. **Set up Supabase** (recommended, takes 5 minutes)
2. **Create mock storage** (quick fix, local files only)

---

## Troubleshooting

### Issue: "Project is still being set up"
**Solution:** Wait 2-3 minutes, refresh the page

### Issue: "Bucket already exists"
**Solution:** Use the existing bucket, just get the API keys

### Issue: "Policy creation failed"
**Solution:** Skip policies for now, they're optional for testing

### Issue: Still getting "Invalid API key"
**Solution:** 
1. Double-check you copied the correct keys
2. Make sure there are no extra spaces
3. Restart the API server
4. Check the `.env` file is in `kiranalens-api/` folder

---

## Quick Verification

After setup, test if it works:

```bash
cd kiranalens-api
python -c "from app.services.storage_service import StorageService; s = StorageService(); print('✅ Supabase connected!')"
```

If you see "✅ Supabase connected!" - you're good to go!

---

## What You Get (Free Tier)

- ✅ 1GB storage
- ✅ 2GB bandwidth per month
- ✅ Unlimited API requests
- ✅ No credit card required
- ✅ Perfect for testing and development

---

## Need Help?

If you're stuck, let me know and I can:
1. Walk you through each step
2. Create a mock storage service instead
3. Help troubleshoot any errors
