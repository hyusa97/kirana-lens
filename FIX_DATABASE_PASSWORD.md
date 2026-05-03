# Fix Database Password

## Current Status

✅ **Supabase Storage is WORKING!** - Images can be uploaded successfully
❌ **Database Connection is FAILING** - Password is incorrect

## The Problem

The database connection is failing with error: **"Tenant or user not found"**

This means the database password in your `.env` file is incorrect.

## How to Fix

### Step 1: Get Your Database Password from Supabase

1. Go to your Supabase project: https://supabase.com/dashboard/project/sjwaszpdqyklqqlgzpja

2. Click on **"Project Settings"** (gear icon in the left sidebar)

3. Click on **"Database"** in the settings menu

4. Scroll down to **"Connection string"**

5. Select **"URI"** tab

6. You'll see a connection string like:
   ```
   postgresql://postgres.sjwaszpdqyklqqlgzpja:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
   ```

7. Copy the password from `[YOUR-PASSWORD]` section

### Step 2: Update Your .env File

1. Open `kiranalens-api/.env`

2. Find the line:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres.sjwaszpdqyklqqlgzpja:KiranaLens%40123@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
   ```

3. Replace `KiranaLens%40123` with your actual password

4. **IMPORTANT:** If your password contains special characters, you need to URL-encode them:
   - `@` becomes `%40`
   - `#` becomes `%23`
   - `$` becomes `%24`
   - `%` becomes `%25`
   - `&` becomes `%26`
   - `+` becomes `%2B`
   - ` ` (space) becomes `%20`

   Example: If password is `MyPass@123`, use `MyPass%40123`

5. Save the file

### Step 3: Restart the API Server

The API server needs to be restarted to load the new password.

## Alternative: Reset Your Database Password

If you don't remember your database password, you can reset it:

1. Go to **Project Settings** → **Database**
2. Scroll to **"Database Password"** section
3. Click **"Reset database password"**
4. Copy the new password
5. Update your `.env` file with the new password (remember to URL-encode special characters!)

## After Fixing

Once you update the password and restart the API server, you should see:

```
[START] Starting KiranaLens API...
[INFO] Database connected successfully!
INFO:     Application startup complete.
```

Instead of:

```
[WARN] Database connection failed: Tenant or user not found
```

## Test It

After fixing, run:
```bash
python test_db_connection.py
```

You should see:
```
✅ DATABASE CONNECTION WORKS!
```

---

**Note:** Even without the database connection, Supabase Storage is working! This means you're very close to having everything working. Just need to fix the database password.
