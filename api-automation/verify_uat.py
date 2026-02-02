"""Simple script to verify UAT connection and create a test user"""

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Get UAT configuration
BASE_URL = os.getenv("BASE_URL", "https://api.uat.teresaapp.com/api/v1")
REGISTER_ENDPOINT = os.getenv("REGISTER_ENDPOINT", "/auth/register")

print(f"🔧 Configuration:")
print(f"   BASE_URL: {BASE_URL}")
print(f"   REGISTER_ENDPOINT: {REGISTER_ENDPOINT}")
print(f"   Full URL: {BASE_URL}{REGISTER_ENDPOINT}")

# Create unique test data
timestamp = int(time.time())
test_data = {
    "f_name": "ManualUAT",
    "l_name": f"TEST_{timestamp}",
    "phone": f"+88017{str(timestamp)[-8:].zfill(8)}",
    "email": f"manual_uat_{timestamp}@test.com",
    "password": "TestPass123!",
    "frontend_url": "https://uat.teresaapp.com/verify"
}

print(f"\n📝 Test Data:")
for key, value in test_data.items():
    if key != "password":
        print(f"   {key}: {value}")
    else:
        print(f"   {key}: {'*' * len(value)}")

# CORRECT ENDPOINT
url = f"{BASE_URL}{REGISTER_ENDPOINT}"
print(f"\n🚀 Sending request to: {url}")

try:
    response = requests.post(
        url,
        json=test_data,
        timeout=15,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "UAT-Verification-Script"
        }
    )
    
    print(f"\n📊 Response:")
    print(f"   Status Code: {response.status_code}")
    
    if response.text:
        print(f"   Response: {response.text}")
    
    if response.status_code == 201:
        print(f"\n✅ SUCCESS! User created in UAT")
        print(f"\n🔍 Verify by:")
        print(f"   1. Postman: GET {BASE_URL}/users?email={test_data['email']}")
        print(f"   2. Admin: https://admin.uat.teresaapp.com")
        print(f"   3. Search for: {test_data['email']}")
        
        # Also suggest checking with correct GET endpoint
        print(f"\n📋 Test User Details:")
        print(f"   Email: {test_data['email']}")
        print(f"   Phone: {test_data['phone']}")
        print(f"   Password: TestPass123!")
        
    elif response.status_code == 422:
        print(f"\n❌ VALIDATION ERROR")
        try:
            error_data = response.json()
            print(f"   Errors: {error_data}")
        except:
            pass
            
    elif response.status_code == 409:
        print(f"\n⚠ USER ALREADY EXISTS (Duplicate)")
        
    else:
        print(f"\n❌ Failed with status: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()