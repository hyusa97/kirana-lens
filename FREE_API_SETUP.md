# Free API Keys Setup Guide

## 1. Groq API (BEST FREE OPTION - Recommended!)

### Setup Steps:
1. Go to https://console.groq.com/
2. Create an account (GitHub/Google sign-in available)
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file:
   ```
   GROQ_API_KEY=gsk_your-actual-groq-key-here
   AI_PROVIDER=groq
   ```

### Free Tier Benefits:
- **FREE**: 14,400 requests per day
- **FAST**: Up to 500+ tokens/second
- **Models Available**:
  - Llama 3.1 70B (best for complex tasks)
  - Llama 3.1 8B (fastest)
  - Mixtral 8x7B (good balance)
- **No credit card required**
- **Perfect for development and production**

## 2. OpenAI API (Alternative)

### Setup Steps:
1. Go to https://platform.openai.com/
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   AI_PROVIDER=openai
   ```

### Free Tier Benefits:
- $5 in free credits for new accounts
- GPT-4o-mini model: ~$0.15 per 1M input tokens
- Perfect for development and testing

## 3. OpenStreetMap with Nominatim (COMPLETELY FREE - Recommended!)

### Setup Steps:
1. **NO SETUP REQUIRED!** 🎉
2. Set in your `.env` file:
   ```
   USE_NOMINATIM=true
   GOOGLE_MAPS_API_KEY=not-needed-with-nominatim
   ```
3. Start using immediately!

### Benefits:
- **100% FREE** - No API key, no registration, no credit card
- **No rate limits** for reasonable use (1 request/second)
- **Global coverage** - Works worldwide
- **Excellent for Indian locations**
- **No ongoing costs** - Ever!

### What You Get:
- Reverse geocoding (coordinates → address)
- Forward geocoding (address → coordinates)  
- Points of interest data
- Business location data
- Neighborhood analysis

### Limitations:
- 1 request per second (automatically handled)
- Slightly slower than Google Maps
- Community-maintained data quality

## 4. Google Maps API (Alternative)

### Setup Steps:
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing one
3. Enable the following APIs:
   - Maps JavaScript API
   - Geocoding API
   - Places API (if needed)
4. Go to "Credentials" and create an API key
5. Add restrictions (recommended):
   - Application restrictions: HTTP referrers
   - API restrictions: Select only the APIs you enabled
6. Copy the key and add it to your `.env` file:
   ```
   USE_NOMINATIM=false
   GOOGLE_MAPS_API_KEY=your-actual-google-maps-key-here
   ```

### Free Tier Benefits:
- $200 monthly credit (resets each month)
- Covers approximately:
  - 28,000 map loads
  - 40,000 geocoding requests
  - 100,000 places searches

## 4. MapBox Alternative

### Setup Steps:
1. Go to https://www.mapbox.com/
2. Create an account
3. Get your access token from the dashboard
4. Add to `.env` file:
   ```
   MAPBOX_ACCESS_TOKEN=your-mapbox-token-here
   ```

### Free Tier Benefits:
- 50,000 map views per month
- 100,000 geocoding requests per month

## Recommended Setup for Development

For development, I **highly recommend this combination**:
1. **Groq API** (FREE, fast, generous limits)
2. **OpenStreetMap Nominatim** (100% free geocoding)

Add these to your `kiranalens-api/.env` file:
```env
# AI Provider
GROQ_API_KEY=gsk-your-groq-key-here
AI_PROVIDER=groq

# Geocoding (100% FREE)
USE_NOMINATIM=true
GOOGLE_MAPS_API_KEY=not-needed-with-nominatim
```

## Cost Estimation

With this **completely free setup**:
- **Groq**: 14,400 requests per day (completely free!)
- **Nominatim**: Unlimited geocoding requests (completely free!)

**Total monthly cost: $0.00** 🎉

This is perfect for development, testing, and even production use!