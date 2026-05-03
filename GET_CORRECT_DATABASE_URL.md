# Get Correct Database URL from Supabase

## Current Issue

The database connection is failing with: **"Tenant or user not found"**

This means either:
1. The password is incorrect
2. The password is not properly URL-encoded
3. The connection string format is wrong

## How to Get the Correct Connection String

### Step 1: Go to Supabase Database Settings

1. Open: https://supabase.com/dashboard/project/sjwaszpdqyklqqlgzpja/settings/database

2. Scroll down to **"Connection string"** section

3. You'll see several tabs: **URI**, **JDBC**, **Prisma**, etc.

### Step 2: Get the Connection String

**Option A: Use the Pooler Connection (Recommended)**

1. Click on **"Connection Pooling"** section (below Connection string)
2. Select **"Transaction"** mode
3. Copy the **URI** connection string
4. It should look like:
   ```
   postgresql://postgres.sjwaszpdqyklqqlgzpja:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
   ```

**Option B: Use Direct Connection**

1. In the **"Connection string"** section
2. Click **"URI"** tab
3. Copy the connection string
4. It should look like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.sjwaszpdqyklqqlgzpja.supabase.co:5432/postgres
   ```

### Step 3: Convert to AsyncPG Format

Take the connection string you copied and:

1. Replace `postgresql://` with `postgresql+asyncpg://`
2. Make sure the password is URL-encoded

**Example:**

If you copied:
```
postgresql://postgres.sjwaszpdqyklqqlgzpja:MyPass@123@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

Convert to:
```
postgresql+asyncpg://postgres.sjwaszpdqyklqqlgzpja:MyPass%40123@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

(Note: `@` became `%40`)

### Step 4: Use the Helper Script

Run this command:
```bash
python encode_password.py
```

It will ask for your password and generate the correct DATABASE_URL for you.

## Common Password Special Characters

If your password contains these characters, they MUST be URL-encoded:

| Character | URL-Encoded |
|-----------|-------------|
| `@`       | `%40`       |
| `#`       | `%23`       |
| `$`       | `%24`       |
| `%`       | `%25`       |
| `&`       | `%26`       |
| `+`       | `%2B`       |
| ` ` (space) | `%20`     |
| `/`       | `%2F`       |
| `?`       | `%3F`       |
| `=`       | `%3D`       |

## Alternative: Reset Your Password

If you're not sure what the password is:

1. Go to: https://supabase.com/dashboard/project/sjwaszpdqyklqqlgzpja/settings/database

2. Scroll to **"Database Password"** section

3. Click **"Reset database password"**

4. Copy the new password (it will be shown once)

5. Use the helper script to encode it:
   ```bash
   python encode_password.py
   ```

6. Update your `.env` file with the generated DATABASE_URL

## Test the Connection

After updating the `.env` file:

1. Restart the API server
2. Run: `python test_db_connection.py`
3. Should see: `✅ DATABASE CONNECTION WORKS!`

## Need Help?

If you're still having issues:

1. Make sure you're copying the password from the correct Supabase project
2. Try resetting the password and using the new one
3. Make sure there are no extra spaces or characters when copying
4. Use the `encode_password.py` script to ensure proper encoding
