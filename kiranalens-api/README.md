# KiranaLens API

AI-powered kirana store cash flow underwriting platform - FastAPI backend

## Features

- ✅ **Async SQLAlchemy 2.0** with asyncpg driver
- ✅ **Alembic** for database migrations
- ✅ **Supabase PostgreSQL** database
- ✅ **Supabase Storage** for image uploads
- ✅ **JWT Authentication** with bcrypt password hashing
- ✅ **Pydantic v2** for validation
- ✅ **CORS** middleware configured
- ✅ **GZip** compression for responses
- ✅ **Health check** endpoint

## Project Structure

```
kiranalens-api/
├── main.py                    # FastAPI app entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── alembic.ini               # Alembic configuration
├── Makefile                  # Development commands
├── alembic/
│   ├── env.py               # Alembic async environment
│   ├── script.py.mako       # Migration template
│   └── versions/            # Migration files
└── app/
    ├── __init__.py
    ├── config.py            # Settings with pydantic-settings
    ├── database.py          # Async SQLAlchemy setup
    ├── dependencies.py      # FastAPI dependencies
    ├── models/              # SQLAlchemy ORM models
    │   ├── __init__.py
    │   ├── user.py
    │   └── assessment.py
    ├── schemas/             # Pydantic schemas
    │   ├── __init__.py
    │   ├── user.py
    │   └── assessment.py
    ├── routers/             # API routes
    │   ├── auth.py
    │   ├── users.py
    │   └── assessments.py
    └── services/            # Business logic
        ├── user_service.py
        ├── assessment_service.py
        └── storage_service.py
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string with asyncpg
- `SECRET_KEY` - JWT secret key
- `ANTHROPIC_API_KEY` - Claude API key
- `GOOGLE_MAPS_API_KEY` - Google Maps API key
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon/service key

### 3. Run Database Migrations

```bash
make migrate
```

Or manually:
```bash
alembic upgrade head
```

### 4. Start Development Server

```bash
make dev
```

Or manually:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Seed Demo Data & Run Tests

```bash
# Run both demo data seeding and smoke tests
python scripts/run_tests.py

# Or run individually:
python scripts/seed_demo_data.py  # Seed demo data
python scripts/smoke_test.py      # Run smoke tests
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## Demo Data

The system includes demo data for testing and development:

**Demo User:**
- Email: `demo@kiranalens.com`
- Password: `Demo@1234`
- Role: Admin

**Demo Assessments:**
1. **Sharma General Store** (Mumbai) - High-performing (CSQS 82.1, Tier A)
2. **Gupta Kirana** (Nagpur) - Medium-performing with risk flags (CSQS 52.4, Tier C)
3. **Lal Dukan** (Rural UP) - Low-performing (CSQS 18.7, Tier E)

## Testing

### Smoke Tests

Run comprehensive API tests:
```bash
python scripts/smoke_test.py
```

Tests include:
- ✅ Health check
- ✅ User registration and login
- ✅ Authentication verification
- ✅ Assessment retrieval
- ✅ Error handling (401, validation)

### Unit Tests

```bash
make test
```

Or manually:
```bash
pytest -v
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/logout` - Logout (client-side token deletion)
- `POST /api/v1/auth/refresh` - Refresh access token

### Users

- `GET /api/v1/users/me` - Get current user info

### Assessments

- `POST /api/v1/assessments` - Create new assessment (multipart/form-data)
- `GET /api/v1/assessments` - Get paginated assessments list
- `GET /api/v1/assessments/{id}` - Get single assessment
- `DELETE /api/v1/assessments/{id}` - Delete assessment
- `POST /api/v1/assessments/{id}/reprocess` - Reprocess assessment
- `GET /api/v1/assessments/{id}/report` - Download PDF report

## Database Migrations

### Create New Migration

```bash
make revision msg="Add new field"
```

Or manually:
```bash
alembic revision --autogenerate -m "Add new field"
```

### Apply Migrations

```bash
make migrate
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Development Commands

```bash
make install    # Install dependencies
make dev        # Run development server
make migrate    # Run database migrations
make revision   # Create new migration
make test       # Run tests
make clean      # Clean Python cache files
```

## Authentication

The API uses JWT Bearer tokens for authentication.

### Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe",
    "organization": "NBFC Ltd",
    "role": "analyst"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "analyst"
  }
}
```

### Use Token

```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Create Assessment

```bash
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "lat=19.0596" \
  -F "lng=72.8295" \
  -F "store_name=Patel Store" \
  -F "gps_accuracy=10" \
  -F "notes=Corner shop" \
  -F "images=@image1.jpg" \
  -F "images=@image2.jpg" \
  -F "images=@image3.jpg"
```

## Database Schema

### Users Table
- `id` (UUID, PK)
- `email` (String, unique)
- `name` (String)
- `organization` (String, nullable)
- `hashed_password` (String)
- `role` (String: analyst, manager, admin)
- `is_active` (Boolean)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Assessments Table
- `id` (UUID, PK)
- `store_name` (String, nullable)
- `address` (Text, nullable)
- `lat` (Float)
- `lng` (Float)
- `gps_accuracy` (Float, nullable)
- `notes` (Text, nullable)
- `csqs` (Integer, nullable)
- `store_tier` (String, nullable)
- `confidence_score` (Integer, nullable)
- `daily_sales_min/max` (Integer, nullable)
- `monthly_revenue_min/max` (Integer, nullable)
- `monthly_income_min/max` (Integer, nullable)
- `signal_breakdown` (JSON, nullable)
- `recommendation` (String, nullable)
- `status` (String)
- `assessed_by` (UUID, FK to users)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `completed_at` (DateTime, nullable)

### Assessment Images Table
- `id` (UUID, PK)
- `assessment_id` (UUID, FK)
- `image_url` (String)
- `image_type` (String, nullable)
- `uploaded_at` (DateTime)

### Risk Flags Table
- `id` (UUID, PK)
- `assessment_id` (UUID, FK)
- `type` (String: high, medium, low)
- `message` (Text)
- `severity` (Integer: 1-5)
- `created_at` (DateTime)

## Testing

### Smoke Tests

Run comprehensive API tests:
```bash
python scripts/smoke_test.py
```

Tests include:
- ✅ Health check
- ✅ User registration and login
- ✅ Authentication verification
- ✅ Assessment retrieval
- ✅ Error handling (401, validation)

### Unit Tests

```bash
make test
```

Or manually:
```bash
pytest -v
```

### Full Test Suite

Run demo data seeding + smoke tests:
```bash
python scripts/run_tests.py
```

## API Documentation

Comprehensive API documentation is available:
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Markdown Docs**: [docs/API.md](docs/API.md)

## Deployment

### Environment Variables

Set all required environment variables in your deployment platform.

### Database

Use Supabase PostgreSQL or any PostgreSQL database with asyncpg support.

### Run Migrations

```bash
alembic upgrade head
```

### Start Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Security

- Passwords are hashed using bcrypt
- JWT tokens expire after 60 minutes (configurable)
- CORS is configured for allowed origins only
- File uploads are validated for size and type
- SQL injection protection via SQLAlchemy ORM

## License

Proprietary - All rights reserved

## Support

For issues or questions, contact the development team.
