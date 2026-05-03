# KiranaLens - Authentication System Documentation

## ✅ Complete Authentication System Implemented

### Overview
A full-featured authentication system with login, registration, protected routes, and session management using Zustand for state management and React Hook Form + Zod for form validation.

---

## 📦 Dependencies Installed

```json
{
  "react-hook-form": "^7.x",
  "zod": "^3.x",
  "@hookform/resolvers": "^3.x",
  "react-hot-toast": "^2.x"
}
```

---

## 🎨 1. Login Page (`/auth/login`)

### Layout
- **Split Layout**: 60% branded panel (left) + 40% login form (right)
- **Branded Panel**: KiranaLens logo, tagline, and 3 feature cards
- **Premium Styling**: Dark navy gradient background

### Form Fields
- **Email**: `type="email"`, placeholder: "you@nbfc.com"
- **Password**: `type="password"` with show/hide toggle
- **Remember Me**: Checkbox
- **Submit Button**: "Sign in" with loading spinner

### Validation (Zod Schema)
```typescript
{
  email: required, valid email format
  password: required, min 8 characters
}
```

### Features
- ✅ Inline error messages on blur
- ✅ Show/hide password toggle
- ✅ Loading state with spinner
- ✅ Toast notification: "Welcome back, [name]!"
- ✅ Redirect to /dashboard on success
- ✅ Link to register page

### Implementation
```typescript
// Login flow
1. User submits form
2. Validate with Zod schema
3. Call api.login(email, password)
4. Set user and token in authStore
5. Set cookie for SSR
6. Show success toast
7. Navigate to /dashboard
```

---

## 📝 2. Register Page (`/auth/register`)

### Layout
- Same split layout as login page
- Branded panel on left, form on right

### Form Fields
1. **Full Name**: Required, min 2 characters
2. **Email**: Required, valid email format
3. **Organisation / NBFC Name**: Required, min 2 characters
4. **Password**: 
   - Min 8 characters
   - Must contain uppercase letter
   - Must contain number
   - Password strength indicator (Weak/Fair/Strong/Very Strong)
5. **Confirm Password**: Must match password
6. **Role**: Select dropdown
   - Credit Officer
   - Branch Manager
   - Admin
7. **Terms Checkbox**: Must be checked

### Password Strength Indicator
- Visual bar with 4 levels
- Color-coded: Red (Weak) → Amber (Fair) → Green (Strong) → Dark Green (Very Strong)
- Real-time feedback as user types

### Validation (Zod Schema)
```typescript
{
  fullName: min 2 chars
  email: valid email
  organization: min 2 chars
  password: min 8 chars + uppercase + number
  confirmPassword: must match password
  role: required enum
  agreeToTerms: must be true
}
```

### Features
- ✅ All fields validated
- ✅ Password strength indicator
- ✅ Show/hide password toggles
- ✅ Inline error messages
- ✅ Success toast on registration
- ✅ Redirect to /auth/login after success

---

## 🔒 3. Auth Guard (middleware.ts)

### Protected Routes
- `/dashboard/*`
- `/assess/*`
- `/admin/*`

### Logic
```typescript
// If no token → redirect to /auth/login
if (isProtectedRoute && !token) {
  redirect('/auth/login?redirect=' + pathname)
}

// If token exists on auth pages → redirect to /dashboard
if (isAuthRoute && token) {
  redirect('/dashboard')
}
```

### Cookie-Based Authentication
- Token stored in cookie: `kiranalens-auth-token`
- Cookie set on login, deleted on logout
- SSR-compatible for middleware checks

---

## 🚪 4. Logout Functionality

### Implementation
Located in Sidebar component:

```typescript
const handleLogout = () => {
  logout();                          // Clear Zustand store
  toast.success('Signed out successfully');
  router.push('/auth/login');        // Redirect to login
};
```

### What Happens
1. Clears user and token from Zustand store
2. Deletes auth cookie
3. Clears localStorage
4. Shows success toast
5. Redirects to login page

---

## 🎨 5. Styling & Design

### Auth Pages
- **Background**: Subtle dark navy gradient (`from-gray-900 via-primary to-gray-900`)
- **Form Card**: Pure white with generous padding, shadow-2xl
- **Border Radius**: 12px for cards, 8px for inputs

### Branded Panel
- **Background**: Primary navy (#1A3A5C)
- **Text**: White with amber accents
- **Features**: 3 cards with icons (Shield, TrendingUp, Zap)
- **Decorative**: Subtle gradient orbs in background

### Form Styling
- **Inputs**: Border on focus, accent ring
- **Buttons**: Accent color with hover state
- **Errors**: Red text below fields
- **Success**: Green toast notifications

---

## 📁 File Structure

```
app/
├── auth/
│   ├── layout.tsx                 # Auth layout (no sidebar)
│   ├── login/page.tsx             # Login page
│   └── register/page.tsx          # Register page
│
components/
├── auth/
│   ├── BrandedPanel.tsx           # Left panel with branding
│   └── PasswordStrength.tsx       # Password strength indicator
├── providers/
│   └── ToastProvider.tsx          # Toast notifications
└── layout/
    ├── Sidebar.tsx                # Updated with logout
    └── TopBar.tsx                 # Updated with user info
│
store/
└── authStore.ts                   # Auth state management
│
middleware.ts                      # Route protection
```

---

## 🔧 Components

### BrandedPanel
```typescript
// Features displayed:
1. AI-Powered Assessment
2. Real-Time Insights
3. Streamlined Workflow

// Includes:
- KiranaLens logo
- Tagline
- Feature cards with icons
- Decorative gradient orbs
```

### PasswordStrength
```typescript
// Calculates strength based on:
- Length (8+ chars, 12+ chars)
- Lowercase letters
- Uppercase letters
- Numbers
- Special characters

// Returns:
- Score: 0-4
- Label: Weak/Fair/Strong/Very Strong
- Color: Red/Amber/Green/Dark Green
```

### ToastProvider
```typescript
// Configuration:
- Position: top-right
- Duration: 3000ms
- Custom styling matching brand colors
- Success/Error icons
```

---

## 🔐 Auth Store (Zustand)

### State
```typescript
{
  user: User | null
  token: string | null
  isAuthenticated: boolean
}
```

### Actions
```typescript
setUser(user)      // Set user and isAuthenticated
setToken(token)    // Set token and cookie
logout()           // Clear everything
```

### Persistence
- Stored in localStorage: `kiranalens-auth-storage`
- Cookie for SSR: `kiranalens-auth-token`
- Survives page refreshes

---

## 🎯 User Flow

### Registration Flow
```
1. User visits /auth/register
2. Fills form with validation
3. Submits form
4. Success toast shown
5. Redirected to /auth/login
6. Can now login with credentials
```

### Login Flow
```
1. User visits /auth/login
2. Enters email and password
3. Form validated
4. API call to login
5. User and token stored
6. Cookie set
7. Welcome toast shown
8. Redirected to /dashboard
```

### Protected Route Access
```
1. User tries to access /dashboard
2. Middleware checks for token cookie
3. If no token → redirect to /auth/login
4. If token exists → allow access
5. User info shown in TopBar
```

### Logout Flow
```
1. User clicks Logout in sidebar
2. Store cleared
3. Cookie deleted
4. Toast shown
5. Redirected to /auth/login
```

---

## 🧪 Testing the System

### Test Login
```
Email: any valid email (e.g., test@nbfc.com)
Password: any 8+ character password
Result: Logged in, redirected to dashboard
```

### Test Registration
```
1. Fill all fields
2. Password must have uppercase + number
3. Confirm password must match
4. Check terms checkbox
5. Submit → Success toast → Redirect to login
```

### Test Protected Routes
```
1. Logout
2. Try to access /dashboard
3. Should redirect to /auth/login
4. Login again
5. Should redirect to /dashboard
```

### Test Logout
```
1. Click Logout in sidebar
2. Toast: "Signed out successfully"
3. Redirected to /auth/login
4. Try to access /dashboard
5. Should redirect back to login
```

---

## 🎨 Design Highlights

### Premium Feel
- Subtle gradient backgrounds
- Generous white space
- Smooth transitions
- Professional color palette

### Branded Panel Features
- **AI-Powered Assessment**: Shield icon
- **Real-Time Insights**: TrendingUp icon
- **Streamlined Workflow**: Zap icon

### Form UX
- Clear labels
- Helpful placeholders
- Inline validation
- Visual feedback
- Loading states

---

## 🔄 Integration with Existing System

### Updated Components
1. **Sidebar**: Now uses authStore for user info and logout
2. **TopBar**: Shows logged-in user name and initials
3. **Root Layout**: Includes ToastProvider
4. **API**: Login/register functions return mock user

### State Management
- Auth state in Zustand store
- Persisted to localStorage
- Cookie for SSR compatibility
- Accessible throughout app

---

## 🚀 Next Steps

### For Production
1. **Real API Integration**
   - Replace mock login/register with real endpoints
   - Add JWT token validation
   - Implement refresh token logic

2. **Enhanced Security**
   - Add CSRF protection
   - Implement rate limiting
   - Add password reset flow
   - Add email verification

3. **Additional Features**
   - Remember me functionality
   - Social login (Google, Microsoft)
   - Two-factor authentication
   - Session timeout warnings

4. **Error Handling**
   - Network error handling
   - Invalid credentials messaging
   - Account locked notifications
   - Password requirements tooltip

---

## 📝 Environment Variables

```env
# Add to .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## ✅ Checklist

- [x] Login page with validation
- [x] Register page with validation
- [x] Password strength indicator
- [x] Show/hide password toggles
- [x] Branded panel component
- [x] Toast notifications
- [x] Auth store with persistence
- [x] Cookie-based auth for SSR
- [x] Middleware for route protection
- [x] Logout functionality
- [x] User info in TopBar
- [x] Premium styling
- [x] Form validation with Zod
- [x] Loading states
- [x] Error messages
- [x] Success toasts
- [x] Redirect logic

---

## 🎉 Authentication System Complete!

The KiranaLens authentication system is now fully functional with:
- ✅ Beautiful login and register pages
- ✅ Complete form validation
- ✅ Protected routes
- ✅ Session management
- ✅ Toast notifications
- ✅ Premium UI/UX

Ready for user testing and real API integration!
