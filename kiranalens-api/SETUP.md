# KiranaLens API - Setup Guide

## Prerequisites

- Python 3.11+
- PostgreSQL (via Supabase or local)
- Supabase account (for storage)
- Anthropic API key (for Claude)
- Google Maps API key

## Step-by-Step Setup

### 1. Create Virtual Environment

```bash
cd kiranalens-api
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Supabase

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your project URL and anon key from Settings > API
4. Create a storage bucket named `kirana-images`:
   - Go to Storage
   - Click "New bucket"
   - Name: `kirana-images`
   - Public: Yes (for image URLs)

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Database - Get from Supabase Settings > Database
DATABASE_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT].supabase.co:5432/postgres

# Security - Generate a random secret key
SECRET_KEY=your-secret-key-here-use-openssl-rand-hex-32

# AI Services
ANTHROPIC_API_KEY=sk-ant-...

# Google Maps
GOOGLE_MAPS_API_KEY=AIza...

# Supabase
SUPABASE_URL=https://[YOUR-PROJECT].supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_BUCKET=kirana-images

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 5. Initialize Database

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 6. Start Development Server

```bash
make dev
```

Or:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Test the API

Open your browser:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 8. Create First User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@kiranalens.com",
    "password": "admin123",
    "name": "Admin User",
    "organization": "KiranaLens",
    "role": "admin"
  }'
```

### 9. Login and Get Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@kiranalens.com",
    "password": "admin123"
  }'
```

Save the `access_token` from the response.

### 10. Test Protected Endpoint

```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Troubleshooting

### Database Connection Error

**Error**: `could not connect to server`

**Solution**:
- Check your DATABASE_URL is correct
- Ensure Supabase project is active
- Check your IP is allowed in Supabase (Settings > Database > Connection Pooling)

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**:
```bash
pip install -r requirements.txt
```

### Alembic Errors

**Error**: `Can't locate revision identified by 'xxx'`

**Solution**:
```bash
# Delete alembic/versions/*.py files
# Recreate initial migration
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### CORS Errors

**Error**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**:
- Add your frontend URL to `ALLOWED_ORIGINS` in `.env`
- Restart the server

## Development Workflow

### 1. Make Model Changes

Edit files in `app/models/`

### 2. Create Migration

```bash
make revision msg="Add new field"
```

### 3. Review Migration

Check `alembic/versions/` for the new migration file

### 4. Apply Migration

```bash
make migrate
```

### 5. Test Changes

```bash
make test
```

## Production Deployment

### 1. Set Environment Variables

Set all variables from `.env.example` in your deployment platform.

### 2. Run Migrations

```bash
alembic upgrade head
```

### 3. Start Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. Use Process Manager

**With Gunicorn**:
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**With Supervisor**:
```ini
[program:kiranalens-api]
command=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
directory=/path/to/kiranalens-api
user=www-data
autostart=true
autorestart=true
```

## Next Steps

1. Connect frontend to API
2. Implement AI processing for assessments
3. Add PDF report generation
4. Set up monitoring and logging
5. Configure CI/CD pipeline

## Support

For issues, check:
- API Docs: http://localhost:8000/docs
- Logs: Check terminal output
- Database: Check Supabase dashboard

Contact: dev@kiranalens.com
