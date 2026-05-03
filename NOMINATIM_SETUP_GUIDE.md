# OpenStreetMap Nominatim Setup Guide - 100% FREE! 🌍

## Why Nominatim?

**OpenStreetMap Nominatim is the BEST FREE geocoding option:**
- ✅ **Completely FREE** - No API key needed
- ✅ **No registration** - Start using immediately  
- ✅ **No rate limits** for reasonable use (1 request/second)
- ✅ **Global coverage** - Works worldwide
- ✅ **Open source** - Community maintained
- ✅ **No credit card** - Ever!

## Quick Setup (2 minutes)

### Step 1: Enable Nominatim in Your .env
Open `kiranalens-api/.env` and set:
```env
# Use OpenStreetMap Nominatim (FREE)
USE_NOMINATIM=true

# Google Maps API key not needed when using Nominatim
GOOGLE_MAPS_API_KEY=not-needed-with-nominatim
```

### Step 2: That's It! 
**No API key needed!** Nominatim is ready to use immediately.

### Step 3: Test It
```bash
# Start your API server
cd kiranalens-api
python main.py

# Test geocoding (it will use Nominatim now)
curl -X POST "http://localhost:8000/api/v1/assessments/" \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 28.6139,
    "longitude": 77.2090,
    "images": ["image1.jpg"]
  }'
```

## How Nominatim Works

### 1. **Reverse Geocoding**
```
https://nominatim.openstreetmap.org/reverse?lat=28.6139&lon=77.2090&format=json
```
- Gets address details from coordinates
- No API key required
- Returns detailed location information

### 2. **Forward Geocoding** 
```
https://nominatim.openstreetmap.org/search?q=New+Delhi&format=json
```
- Gets coordinates from address
- Perfect for address validation
- Supports multiple languages

### 3. **Overpass API Integration**
- Uses OpenStreetMap's Overpass API for POI data
- Finds nearby businesses, schools, hospitals
- Completely free and comprehensive

## What Your App Gets with Nominatim

### ✅ **Geographic Analysis Features:**
1. **Road Type Analysis** - Identifies road types and accessibility
2. **Competition Density** - Finds nearby grocery stores and competitors  
3. **Footfall Proxy** - Counts schools, hospitals, offices nearby
4. **Catchment Density** - Analyzes residential vs commercial areas
5. **Neighbourhood Quality** - Assesses area based on address completeness

### ✅ **Data Sources:**
- **Nominatim API** - Address and location details
- **Overpass API** - Points of interest and business data
- **OpenStreetMap** - Global map data maintained by community

## Rate Limits & Best Practices

### **Rate Limits:**
- **1 request per second** (automatically handled in code)
- **No daily limits**
- **No monthly quotas**
- **Fair use policy** - don't abuse the service

### **Best Practices:**
- ✅ Include User-Agent header (already implemented)
- ✅ Respect 1 request/second limit (built into code)
- ✅ Cache results when possible
- ✅ Don't make bulk requests

## Comparison: Nominatim vs Google Maps

| Feature | Nominatim (FREE) | Google Maps |
|---------|------------------|-------------|
| **Cost** | 100% Free | $200/month free, then paid |
| **API Key** | Not needed | Required |
| **Rate Limits** | 1 req/sec | 1000 req/day free |
| **Global Coverage** | Excellent | Excellent |
| **POI Data** | Very good | Excellent |
| **Address Quality** | Good | Excellent |
| **Setup Time** | 2 minutes | 10 minutes |

## Advanced Configuration

### Custom Nominatim Instance
If you need higher rate limits, you can run your own Nominatim server:

```env
# Use custom Nominatim instance
NOMINATIM_BASE_URL=https://your-nominatim-server.com
```

### Hybrid Approach
Use both services for maximum reliability:

```env
# Primary: Nominatim (free)
USE_NOMINATIM=true

# Fallback: Google Maps (if Nominatim fails)
GOOGLE_MAPS_API_KEY=your-google-key-here
```

## Troubleshooting

### "Too Many Requests" Error
- You're exceeding 1 request/second
- The code automatically adds delays
- Check for concurrent requests

### "No Results" for Address
- Try different address formats
- Use coordinates instead of addresses
- Check if location exists in OpenStreetMap

### Slow Response Times
- Nominatim can be slower than Google (2-5 seconds)
- Consider caching results
- Use coordinates when possible (faster than addresses)

## Sample API Responses

### Reverse Geocoding Response:
```json
{
  "place_id": 123456,
  "licence": "© OpenStreetMap contributors",
  "display_name": "New Delhi, Delhi, India",
  "address": {
    "city": "New Delhi",
    "state": "Delhi", 
    "country": "India",
    "postcode": "110001"
  },
  "lat": "28.6139391",
  "lon": "77.2090212"
}
```

### Overpass POI Response:
```json
{
  "elements": [
    {
      "type": "node",
      "id": 123,
      "lat": 28.6139,
      "lon": 77.2090,
      "tags": {
        "amenity": "school",
        "name": "Local School"
      }
    }
  ]
}
```

## Why This is Perfect for Your App

### **For Development:**
- ✅ Start building immediately
- ✅ No API key management
- ✅ No billing concerns
- ✅ Full feature testing

### **For Production:**
- ✅ No ongoing costs
- ✅ Reliable service
- ✅ Global coverage
- ✅ Community support

### **For Indian Markets:**
- ✅ Good coverage of Indian cities
- ✅ Local business data
- ✅ Hindi/regional language support
- ✅ No foreign exchange concerns

## Next Steps

1. ✅ Set `USE_NOMINATIM=true` in your .env
2. ✅ Test your first geocoding request
3. 🚀 Deploy with confidence - no API costs!
4. 📈 Scale without worrying about geocoding bills

**You now have completely free, unlimited geocoding!** 🎉