# KiranaLens API Scripts

This directory contains utility scripts for testing and demo data management.

## Scripts

### 1. Demo Data Seeding (`seed_demo_data.py`)

Seeds the database with 3 fully-processed demo assessments and a demo user for testing.

**Demo Data:**
- **Demo User**: `demo@kiranalens.com` / `Demo@1234` (Admin role)
- **Sharma General Store** (Mumbai): High-performing store (CSQS 82.1, Tier A)
- **Gupta Kirana** (Nagpur): Medium-performing store with risk flags (CSQS 52.4, Tier C)
- **Lal Dukan** (Rural UP): Low-performing store (CSQS 18.7, Tier E)

**Usage:**
```bash
cd kiranalens-api
python scripts/seed_demo_data.py
```

**Prerequisites:**
- Database must be running and accessible
- Environment variables must be configured in `.env`

### 2. Smoke Tests (`smoke_test.py`)

Runs comprehensive HTTP tests against the API to verify core functionality.

**Tests Included:**
1. ✅ GET /health → 200, status='ok'
2. ✅ POST /api/v1/auth/register → 201
3. ✅ POST /api/v1/auth/login → 200, has access_token
4. ✅ GET /api/v1/auth/me → 200, correct email
5. ✅ GET /api/v1/assessments → 200, list with total
6. ✅ GET /api/v1/assessments/{demo_id_1} → 200, csqs=82.1
7. ✅ GET /api/v1/assessments/{demo_id_1}/status → 200, status='complete'
8. ✅ POST /api/v1/auth/login (wrong password) → 401
9. ✅ GET /api/v1/assessments (no token) → 401

**Usage:**
```bash
cd kiranalens-api
python scripts/smoke_test.py
```

**Prerequisites:**
- API server must be running on `http://localhost:8000`
- Demo data should be seeded first for complete testing

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API server:**
   ```bash
   python main.py
   ```

3. **Seed demo data:**
   ```bash
   python scripts/seed_demo_data.py
   ```

4. **Run smoke tests:**
   ```bash
   python scripts/smoke_test.py
   ```

## Expected Output

### Demo Data Seeding
```
🌱 Starting demo data seeding...
🔧 Creating demo user...
   ✅ Created demo user: demo@kiranalens.com
🏪 Creating Demo 1: Sharma General Store...
   ✅ Created assessment: Sharma General Store (CSQS: 82.1)
🏪 Creating Demo 2: Gupta Kirana...
   ✅ Created assessment: Gupta Kirana (CSQS: 52.4)
🏪 Creating Demo 3: Lal Dukan...
   ✅ Created assessment: Lal Dukan (CSQS: 18.7)

✅ Demo data seeding completed successfully!

📊 Summary:
   👤 Demo user: demo@kiranalens.com (password: Demo@1234)
   🏪 Sharma General Store: CSQS 82.1 (Tier A)
   🏪 Gupta Kirana: CSQS 52.4 (Tier C)
   🏪 Lal Dukan: CSQS 18.7 (Tier E)

🚀 You can now run smoke tests with: python scripts/smoke_test.py
```

### Smoke Tests
```
🧪 Starting KiranaLens API Smoke Tests
Target: http://localhost:8000
==================================================

[PASS] GET /health → 200, status='ok'
       Status: ok, DB: True
[PASS] POST /api/v1/auth/register → 201
       Created user: smoketest_abc123@test.com
[PASS] POST /api/v1/auth/login → 200, has access_token
       Token type: bearer
[PASS] GET /api/v1/auth/me → 200, correct email
       User: Smoke Test User (credit_officer)
[PASS] GET /api/v1/assessments → 200, list with total
       Found 3 assessments
[PASS] GET /api/v1/assessments/{demo_id_1} → 200, csqs=82.1
       CSQS: 82.1, Store: Sharma General Store
[PASS] GET /api/v1/assessments/{demo_id_1}/status → 200, status='complete'
       Status: complete
[PASS] POST /api/v1/auth/login (wrong password) → 401
       Correctly rejected invalid credentials
[PASS] GET /api/v1/assessments (no token) → 401
       Correctly rejected unauthenticated request

==================================================
ALL TESTS PASSED! 🎉
9/9 tests passed
==================================================
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in `.env` file
   - Verify database credentials

2. **API Server Not Running**
   - Start the server with `python main.py`
   - Check if port 8000 is available
   - Verify no firewall blocking

3. **Import Errors**
   - Install dependencies: `pip install -r requirements.txt`
   - Ensure you're in the correct directory
   - Check Python path configuration

4. **Demo Data Already Exists**
   - Scripts handle existing data gracefully
   - Demo user will be reused if already exists
   - Assessments are created with unique IDs

5. **Smoke Tests Fail**
   - Ensure demo data is seeded first
   - Check API server is accessible
   - Verify all endpoints are working

### Environment Variables

Ensure these are set in your `.env` file:
```env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
SUPABASE_URL=https://...
SUPABASE_KEY=...
GROQ_API_KEY=... (or other AI provider)
```

## Development

To modify or extend these scripts:

1. **Adding New Demo Data:**
   - Edit `seed_demo_data.py`
   - Add new assessment creation functions
   - Update the summary output

2. **Adding New Tests:**
   - Edit `smoke_test.py`
   - Add new test methods to `SmokeTestRunner`
   - Update the test count in summary

3. **Configuration:**
   - Modify `BASE_URL` in smoke_test.py for different environments
   - Adjust timeout values if needed
   - Customize test user credentials