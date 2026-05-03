# Groq API Setup Guide - FREE & FAST! 🚀

## Why Groq?

Groq is the **BEST FREE option** for AI inference:
- ✅ **Completely FREE**: 14,400 requests per day
- ✅ **Lightning Fast**: Up to 500+ tokens/second
- ✅ **No Credit Card**: Sign up with just email/GitHub
- ✅ **Production Ready**: Reliable and stable
- ✅ **Great Models**: Llama 3.1 70B, Mixtral, and more

## Quick Setup (5 minutes)

### Step 1: Get Your Groq API Key
1. Go to https://console.groq.com/
2. Sign up with GitHub/Google (no credit card needed!)
3. Click "API Keys" in the left sidebar
4. Click "Create API Key"
5. Copy your key (starts with `gsk_`)

### Step 2: Update Your .env File
Open `kiranalens-api/.env` and add:
```env
# Set Groq as your AI provider
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_groq_key_here

# You can leave these empty when using Groq
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

### Step 3: Install Dependencies
```bash
cd kiranalens-api
pip install groq==0.4.1
```

### Step 4: Test It!
```bash
# Start your API server
python main.py

# Test the vision endpoint (it will use Groq now)
curl -X POST "http://localhost:8000/api/v1/assessments/" \
  -H "Authorization: Bearer your_jwt_token" \
  -F "images=@test_image.jpg"
```

## Available Models on Groq

| Model | Best For | Speed | Context |
|-------|----------|-------|---------|
| `llama-3.1-70b-versatile` | Complex analysis (default) | Fast | 128K tokens |
| `llama-3.1-8b-instant` | Simple tasks | Ultra-fast | 128K tokens |
| `mixtral-8x7b-32768` | Balanced performance | Fast | 32K tokens |

## Free Tier Limits

- **14,400 requests per day** (resets daily)
- **No monthly limits**
- **No credit card required**
- **No expiration**

This is perfect for:
- Development and testing
- Small to medium production apps
- Prototyping
- Educational projects

## Switching Between Providers

You can easily switch between AI providers by changing the `AI_PROVIDER` in your `.env`:

```env
# Use Groq (FREE - recommended)
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here

# Or use OpenAI
AI_PROVIDER=openai
OPENAI_API_KEY=sk_your_key_here

# Or use Anthropic
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
```

## Important Notes

### Vision Analysis with Groq
- Groq doesn't support vision models yet
- The system will use text-based analysis as a fallback
- For full vision capabilities, use OpenAI or Anthropic
- We're working on integrating vision through other services

### Rate Limits
- 14,400 requests/day = ~600 requests/hour
- Perfect for most applications
- No burst limits - use as fast as you need

### Error Handling
The system automatically handles:
- API key validation
- Rate limit errors
- Model switching
- Fallback responses

## Troubleshooting

### "Invalid API Key" Error
1. Check your API key starts with `gsk_`
2. Verify it's correctly set in `.env`
3. Make sure there are no extra spaces

### "Rate Limit Exceeded"
1. You've used your daily 14,400 requests
2. Wait until the next day (resets at midnight UTC)
3. Or switch to OpenAI/Anthropic temporarily

### "Model Not Found"
1. Check the model name in `vision_service.py`
2. Verify Groq supports the model
3. Try switching to `llama-3.1-8b-instant`

## Cost Comparison

| Provider | Free Tier | Cost After Free |
|----------|-----------|-----------------|
| **Groq** | 14,400 req/day | Still researching pricing |
| OpenAI | $5 credit | $0.15-$0.60 per 1M tokens |
| Anthropic | No free tier | $3-$15 per 1M tokens |

**Winner: Groq** - Best free tier, fastest inference!

## Next Steps

1. ✅ Set up Groq API key
2. ✅ Test your first request
3. 🔄 Consider adding Google Maps API for geocoding
4. 🚀 Deploy your app with free AI inference!

Need help? Check the main `FREE_API_SETUP.md` for more options!