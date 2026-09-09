#test configuration settings

from app.core.config import settings

print("=" * 40)
print("Configuration Test")
print("=" * 40)

print(f"App Name: {settings.app_name}")
print(f"Environment: {settings.environment}")
print(f"Database URL: {settings.database_url}")
print(f"JWT Algorithm: {settings.algorithm}")
print(f"Token Expiry: {settings.access_token_expire_minutes}")

print("\nConfiguration loaded successfully!")