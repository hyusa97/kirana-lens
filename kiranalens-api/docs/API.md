# KiranaLens API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
The API uses JWT Bearer token authentication. Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Health Check

#### GET /health
Check API health status and service availability.

**Auth Required:** No

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "db_connected": true,
  "checks": {
    "database": "healthy",
    "storage": "healthy"
  }
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/health"
```

---

### Authentication

#### POST /api/v1/auth/register
Register a new user account.

**Auth Required:** No

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "organisation": "ABC Bank",
  "password": "SecurePass123",
  "role": "credit_officer"
}
```

**Response (201):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "john@example.com",
  "name": "John Doe",
  "organisation": "ABC Bank",
  "role": "credit_officer",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "organisation": "ABC Bank",
    "password": "SecurePass123",
    "role": "credit_officer"
  }'
```

#### POST /api/v1/auth/login
Authenticate user and get access tokens.

**Auth Required:** No

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "john@example.com",
    "name": "John Doe",
    "organisation": "ABC Bank",
    "role": "credit_officer",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

#### GET /api/v1/auth/me
Get current user information.

**Auth Required:** Yes

**Response (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "john@example.com",
  "name": "John Doe",
  "organisation": "ABC Bank",
  "role": "credit_officer",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <access_token>"
```

#### POST /api/v1/auth/refresh
Refresh access token using refresh token.

**Auth Required:** No

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

#### POST /api/v1/auth/logout
Logout current user (client-side token removal).

**Auth Required:** Yes

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer <access_token>"
```

---

### Assessments

#### POST /api/v1/assessments
Create a new assessment with store images.

**Auth Required:** Yes

**Request Body (multipart/form-data):**
- `lat` (float): Latitude coordinate (-90 to 90)
- `lng` (float): Longitude coordinate (-180 to 180)
- `store_name` (string, optional): Store name
- `gps_accuracy_metres` (float, optional): GPS accuracy in metres
- `images` (files): 3-5 image files (max 10MB each)

**Response (201):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "user_id": "123e4567-e89b-12d3-a456-426614174001",
  "store_name": "Sharma General Store",
  "address": null,
  "lat": "19.1136",
  "lng": "72.8697",
  "gps_accuracy_metres": 5.0,
  "image_urls": [
    "https://storage.supabase.co/v1/object/public/kirana-images/image1.jpg"
  ],
  "status": "pending",
  "error_message": null,
  "csqs": null,
  "store_tier": null,
  "confidence_score": null,
  "daily_sales_min": null,
  "daily_sales_max": null,
  "monthly_revenue_min": null,
  "monthly_revenue_max": null,
  "monthly_income_min": null,
  "monthly_income_max": null,
  "risk_flags": [],
  "recommendation": null,
  "signal_breakdown": null,
  "pdf_report_url": null,
  "visual_features": null,
  "geo_features": null
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/assessments" \
  -H "Authorization: Bearer <access_token>" \
  -F "lat=19.1136" \
  -F "lng=72.8697" \
  -F "store_name=Sharma General Store" \
  -F "gps_accuracy_metres=5.0" \
  -F "images=@store_exterior.jpg" \
  -F "images=@store_interior.jpg" \
  -F "images=@store_shelves.jpg"
```

#### GET /api/v1/assessments
Get paginated list of assessments.

**Auth Required:** Yes

**Query Parameters:**
- `page` (int, default=1): Page number
- `limit` (int, default=20): Items per page
- `status_filter` (string, optional): Filter by status (pending, processing, complete, error)
- `store_tier` (string, optional): Filter by tier (A, B, C, D, E)
- `recommendation` (string, optional): Filter by recommendation (pre_approve, needs_verification, reject)

**Response (200):**
```json
{
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:35:00Z",
      "user_id": "123e4567-e89b-12d3-a456-426614174001",
      "store_name": "Sharma General Store",
      "address": "Shop 15, Andheri West, Mumbai",
      "lat": "19.1136",
      "lng": "72.8697",
      "gps_accuracy_metres": 5.0,
      "image_urls": ["https://storage.supabase.co/..."],
      "status": "complete",
      "error_message": null,
      "csqs": "82.1",
      "store_tier": "A",
      "confidence_score": "0.87",
      "daily_sales_min": 8000,
      "daily_sales_max": 15000,
      "monthly_revenue_min": 240000,
      "monthly_revenue_max": 450000,
      "monthly_income_min": 36000,
      "monthly_income_max": 67500,
      "risk_flags": [],
      "recommendation": "pre_approve",
      "signal_breakdown": {
        "shelf_density_index": 88.5,
        "sku_diversity_score": 92.3
      },
      "pdf_report_url": null,
      "visual_features": null,
      "geo_features": null
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20,
  "pages": 1
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/assessments?page=1&limit=10&status_filter=complete" \
  -H "Authorization: Bearer <access_token>"
```

#### GET /api/v1/assessments/{assessment_id}
Get single assessment by ID with full details.

**Auth Required:** Yes

**Path Parameters:**
- `assessment_id` (UUID): Assessment ID

**Response (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "user_id": "123e4567-e89b-12d3-a456-426614174001",
  "store_name": "Sharma General Store",
  "address": "Shop 15, Andheri West, Mumbai",
  "lat": "19.1136",
  "lng": "72.8697",
  "gps_accuracy_metres": 5.0,
  "image_urls": ["https://storage.supabase.co/..."],
  "status": "complete",
  "error_message": null,
  "csqs": "82.1",
  "store_tier": "A",
  "confidence_score": "0.87",
  "daily_sales_min": 8000,
  "daily_sales_max": 15000,
  "monthly_revenue_min": 240000,
  "monthly_revenue_max": 450000,
  "monthly_income_min": 36000,
  "monthly_income_max": 67500,
  "risk_flags": [],
  "recommendation": "pre_approve",
  "signal_breakdown": {
    "shelf_density_index": 88.5,
    "sku_diversity_score": 92.3,
    "inventory_value_band": 85.7,
    "refill_signal": 78.9,
    "store_organization_score": 91.2,
    "counter_activity_proxy": 84.6,
    "exterior_quality_score": 89.1,
    "road_type_score": 95.2,
    "catchment_density_score": 87.4,
    "footfall_proxy_index": 93.8,
    "competition_density_score": 76.3,
    "neighbourhood_quality_score": 88.7
  },
  "pdf_report_url": null,
  "visual_features": {
    "id": "123e4567-e89b-12d3-a456-426614174002",
    "assessment_id": "123e4567-e89b-12d3-a456-426614174000",
    "shelf_density_index": 89,
    "sku_diversity_score": 92,
    "store_organization_score": 91,
    "counter_activity_proxy": 85,
    "exterior_quality_score": 89,
    "inventory_value_band": "high",
    "refill_signal": "normal",
    "image_quality_warnings": [],
    "created_at": "2024-01-15T10:35:00Z"
  },
  "geo_features": {
    "id": "123e4567-e89b-12d3-a456-426614174003",
    "assessment_id": "123e4567-e89b-12d3-a456-426614174000",
    "road_type_score": 95,
    "catchment_density_score": 87,
    "footfall_proxy_index": 94,
    "competition_density_score": 76,
    "neighbourhood_quality_score": 89,
    "competitor_count": 3,
    "poi_count": 12,
    "created_at": "2024-01-15T10:35:00Z"
  }
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/assessments/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer <access_token>"
```

#### GET /api/v1/assessments/{assessment_id}/status
Get assessment status for polling during processing.

**Auth Required:** Yes

**Path Parameters:**
- `assessment_id` (UUID): Assessment ID

**Response (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "complete",
  "progress_step": "Analysis complete",
  "error_message": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/assessments/123e4567-e89b-12d3-a456-426614174000/status" \
  -H "Authorization: Bearer <access_token>"
```

#### POST /api/v1/assessments/{assessment_id}/reprocess
Reprocess an existing assessment (Admin only).

**Auth Required:** Yes (Admin role + API key)

**Path Parameters:**
- `assessment_id` (UUID): Assessment ID

**Headers:**
- `X-API-Key`: Internal API key

**Response (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing",
  "message": "Assessment queued for reprocessing"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/assessments/123e4567-e89b-12d3-a456-426614174000/reprocess" \
  -H "Authorization: Bearer <admin_access_token>" \
  -H "X-API-Key: <internal_api_key>"
```

---

### Users

#### GET /api/v1/users
Get paginated list of users (Admin only).

**Auth Required:** Yes (Admin role)

**Query Parameters:**
- `page` (int, default=1): Page number
- `limit` (int, default=20): Items per page

**Response (200):**
```json
{
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "john@example.com",
      "name": "John Doe",
      "organisation": "ABC Bank",
      "role": "credit_officer",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20,
  "pages": 1
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/users" \
  -H "Authorization: Bearer <admin_access_token>"
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "lat",
      "message": "ensure this value is greater than or equal to -90",
      "type": "value_error.number.not_ge"
    }
  ],
  "request_id": "req_123456"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials",
  "status_code": 401,
  "request_id": "req_123456"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions",
  "status_code": 403,
  "request_id": "req_123456"
}
```

### 404 Not Found
```json
{
  "detail": "Assessment not found",
  "status_code": 404,
  "request_id": "req_123456"
}
```

### 409 Conflict
```json
{
  "detail": "Email already registered",
  "status_code": 409,
  "request_id": "req_123456"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "email",
      "message": "field required",
      "type": "value_error.missing"
    }
  ],
  "request_id": "req_123456"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded: 5 per minute",
  "status_code": 429,
  "request_id": "req_123456"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "request_id": "req_123456"
}
```

---

## Rate Limits

- **Authentication endpoints**: 5 requests per minute per IP
- **Assessment creation**: 10 requests per hour per user
- **General GET endpoints**: 100 requests per minute per user
- **General endpoints**: 60 requests per minute per IP

---

## Data Models

### User Roles
- `credit_officer`: Standard user role
- `branch_manager`: Manager role with additional permissions
- `admin`: Full administrative access

### Assessment Status
- `pending`: Assessment created, waiting for processing
- `processing`: AI analysis in progress
- `complete`: Analysis completed successfully
- `error`: Processing failed

### Store Tiers
- `A`: Premium stores (CSQS 80-100)
- `B`: High-quality stores (CSQS 60-79)
- `C`: Average stores (CSQS 40-59)
- `D`: Below-average stores (CSQS 20-39)
- `E`: Poor-performing stores (CSQS 0-19)

### Recommendations
- `pre_approve`: Recommended for loan approval
- `needs_verification`: Requires manual review
- `reject`: Not recommended for loan approval

### Risk Flags
- `gps_accuracy_low`: GPS accuracy below threshold
- `competitor_saturation`: High competition in area
- `refill_signal_overfilled`: Inventory management concerns
- `image_quality_poor`: Image quality issues affecting analysis

---

## Getting Started

1. **Start the API server:**
   ```bash
   cd kiranalens-api
   python main.py
   ```

2. **Register a user:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test User",
       "email": "test@example.com",
       "password": "TestPass123",
       "role": "credit_officer"
     }'
   ```

3. **Login and get token:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "TestPass123"
     }'
   ```

4. **Create an assessment:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/assessments" \
     -H "Authorization: Bearer <access_token>" \
     -F "lat=19.1136" \
     -F "lng=72.8697" \
     -F "store_name=Test Store" \
     -F "images=@store_image.jpg"
   ```

5. **Check assessment status:**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/assessments/<assessment_id>/status" \
     -H "Authorization: Bearer <access_token>"
   ```

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints directly in your browser.