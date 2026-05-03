"""
Test database connection directly
"""
import asyncio
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv('kiranalens-api/.env')

DATABASE_URL = os.getenv('DATABASE_URL')

# Convert asyncpg URL format
db_url = DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')

print("=" * 60)
print("DATABASE CONNECTION TEST")
print("=" * 60)
print(f"\nDatabase URL: {db_url[:50]}...")

async def test_connection():
    try:
        print("\n1. Attempting to connect...")
        conn = await asyncpg.connect(db_url)
        print("✅ Connection successful!")
        
        print("\n2. Testing query...")
        result = await conn.fetchval('SELECT version()')
        print(f"✅ PostgreSQL version: {result[:50]}...")
        
        await conn.close()
        print("\n" + "=" * 60)
        print("✅ DATABASE CONNECTION WORKS!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print(f"   Type: {type(e).__name__}")
        print("\n" + "=" * 60)
        print("❌ DATABASE CONNECTION FAILED")
        print("=" * 60)
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
