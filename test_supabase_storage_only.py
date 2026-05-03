"""
Test Supabase Storage directly without database
"""
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('kiranalens-api/.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET')

print("=" * 60)
print("SUPABASE STORAGE DIRECT TEST")
print("=" * 60)

print(f"\nSupabase URL: {SUPABASE_URL}")
print(f"Supabase Key: {SUPABASE_KEY[:20]}...")
print(f"Bucket: {SUPABASE_BUCKET}")

try:
    print("\n1. Creating Supabase client...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Client created successfully!")
    
    print("\n2. Testing storage access...")
    # Create a small test image
    test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    
    filename = "test/test-image.png"
    
    print(f"3. Uploading test image to {SUPABASE_BUCKET}/{filename}...")
    response = supabase.storage.from_(SUPABASE_BUCKET).upload(
        path=filename,
        file=test_image,
        file_options={
            "content-type": "image/png",
            "cache-control": "3600",
            "upsert": "true"  # Overwrite if exists
        }
    )
    
    print(f"   Upload response: {response}")
    
    print("\n4. Getting public URL...")
    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)
    print(f"   Public URL: {public_url}")
    
    print("\n" + "=" * 60)
    print("✅ SUPABASE STORAGE IS WORKING!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print(f"   Type: {type(e).__name__}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
    print("\n" + "=" * 60)
    print("❌ SUPABASE STORAGE TEST FAILED")
    print("=" * 60)
