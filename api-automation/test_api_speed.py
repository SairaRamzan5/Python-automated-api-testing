# test_api_speed.py
import requests
import time
import random

BASE_URL = "https://api.uat.teresaapp.com/api/v1"

def test_api_speed():
    """Test API response time"""
    print("Testing API response time...")
    
    # Test 1: Simple GET request (health check if available)
    try:
        start = time.time()
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        elapsed = time.time() - start
        print(f"1. Health check: {response.status_code} in {elapsed:.2f}s")
    except:
        print("1. Health check endpoint not available or timed out")
    
    # Test 2: Registration request
    phone = f"+88017{''.join([str(random.randint(0, 9)) for _ in range(8)])}"
    email = f"speed_test_{int(time.time())}@test.com"
    
    data = {
        "f_name": "Speed",
        "l_name": "Test",
        "phone": phone,
        "email": email,
        "password": "Test@123",
        "frontend_url": "https://uat.teresaapp.com/verify"
    }
    
    print(f"\nTesting registration with:")
    print(f"  Phone: {phone}")
    print(f"  Email: {email}")
    
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/auth/register", 
                                json=data, 
                                timeout=30)
        elapsed = time.time() - start
        print(f"\n2. Registration: {response.status_code} in {elapsed:.2f}s")
        print(f"   Response: {response.text[:200]}")
    except requests.exceptions.Timeout:
        print(f"\n2. Registration: TIMEOUT after 30 seconds")
    except Exception as e:
        print(f"\n2. Registration: ERROR - {e}")

if __name__ == "__main__":
    test_api_speed()