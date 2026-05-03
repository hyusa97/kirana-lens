"""
Helper script to URL-encode your database password
"""
from urllib.parse import quote_plus

print("=" * 60)
print("DATABASE PASSWORD URL ENCODER")
print("=" * 60)

print("\nThis script will help you URL-encode your database password.")
print("Enter your password exactly as shown in Supabase.")
print()

password = input("Enter your database password: ")

# URL encode the password
encoded_password = quote_plus(password)

print("\n" + "=" * 60)
print("ENCODED PASSWORD")
print("=" * 60)
print(f"\nOriginal: {password}")
print(f"Encoded:  {encoded_password}")

# Generate the full DATABASE_URL
database_url = f"postgresql+asyncpg://postgres.sjwaszpdqyklqqlgzpja:{encoded_password}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

print("\n" + "=" * 60)
print("FULL DATABASE_URL")
print("=" * 60)
print(f"\n{database_url}")

print("\n" + "=" * 60)
print("INSTRUCTIONS")
print("=" * 60)
print("\n1. Copy the DATABASE_URL above")
print("2. Open kiranalens-api/.env")
print("3. Replace the DATABASE_URL line with the one above")
print("4. Save the file")
print("5. Restart the API server")
print("\n" + "=" * 60)
