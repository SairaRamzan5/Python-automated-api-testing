"""Simple pytest configuration - MINIMAL VERSION"""

import pytest
import time
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope="function")
def api_client():
    """Fixture to provide API client instance for UAT"""
    from api.client import APIClient
    from config.settings import settings
    
    client = APIClient(base_url=settings.BASE_URL)
    
    yield client
    
    # Cleanup after test
    client.clear_auth_token()

@pytest.fixture(scope="function")  # CHANGED: function scope to match api_client
def admin_auth_token(api_client):
    """Get admin authentication token"""
    from api.endpoints import Endpoints
    from config.settings import settings
    
    print("\n   Getting admin token...")
    
    login_data = {
        "identifier": settings.ADMIN_EMAIL,
        "password": settings.ADMIN_PASSWORD
    }
    
    try:
        response = api_client.post(Endpoints.LOGIN, json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                token = data.get("data", {}).get("access_token")
                if token:
                    print(f"   ✓ Admin token obtained")
                    return token
                else:
                    print(f"   ⚠ No token in response")
            else:
                print(f"   ⚠ Login failed: {data.get('message')}")
        else:
            print(f"   ⚠ Login failed with status: {response.status_code}")
            if response.text:
                print(f"     Response: {response.text[:200]}")
    
    except Exception as e:
        print(f"   ❌ Error getting admin token: {e}")
    
    return None

@pytest.fixture(scope="function")  # CHANGED: function scope
def artisan_credentials():
    """Get artisan credentials from environment variables"""
    return {
        "phone": os.getenv("ARTISAN_PHONE"),
        "password": os.getenv("ARTISAN_PASSWORD")
    }

@pytest.fixture(scope="function")  # CHANGED: function scope to match api_client
def artisan_auth_token(api_client, artisan_credentials):
    """Get artisan authentication token"""
    phone = artisan_credentials["phone"]
    password = artisan_credentials["password"]
    
    if not phone or not password:
        print("   ⚠ Artisan credentials not found in environment variables")
        return None
    
    print(f"   Getting artisan token for phone: {phone[:4]}****")
    
    login_data = {
        "phone": phone,
        "password": password
    }
    
    try:
        # Try different possible login endpoints for artisan
        login_endpoints = [
            "/auth/login",
            "/artisan/login", 
            "/login/artisan",
            "/auth/artisan/login"
        ]
        
        token = None
        successful_endpoint = None
        
        for endpoint in login_endpoints:
            try:
                response = api_client.post(endpoint, json=login_data)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        token = data.get("data", {}).get("access_token") or data.get("data", {}).get("token")
                        if token:
                            successful_endpoint = endpoint
                            break
            except:
                continue  # Try next endpoint
        
        if token:
            print(f"   ✓ Artisan token obtained from {successful_endpoint}")
            return token
        else:
            print(f"   ⚠ Could not get artisan token from any endpoint")
    
    except Exception as e:
        print(f"   ⚠ Error getting artisan token: {e}")
    
    return None

@pytest.fixture(scope="session", autouse=True)
def session_setup():
    """Session setup - runs once at the start"""
    from config.settings import settings
    
    print(f"\n{'='*80}")
    print(f"Starting UAT Test Session")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Base URL: {settings.BASE_URL}")
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    yield
    
    print(f"\n{'='*80}")
    print(f"Test Session Complete")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")

@pytest.fixture(autouse=True)
def test_delay():
    """Add small delay between tests to prevent rate limiting"""
    yield
    from config.settings import settings
    time.sleep(settings.TEST_DELAY if hasattr(settings, 'TEST_DELAY') else 1.0)

@pytest.fixture(scope="function")
def artisan_credentials():
    """Get artisan credentials from environment variables"""
    # Try both possible identifier names
    identifier = os.getenv("ARTISAN_IDENTIFIER") or os.getenv("ARTISAN_PHONE") or os.getenv("ARTISAN_EMAIL")
    password = os.getenv("ARTISAN_PASSWORD")
    
    if not identifier or not password:
        print("   ⚠ Artisan credentials not found in environment variables")
        print("   Add ARTISAN_IDENTIFIER and ARTISAN_PASSWORD to .env file")
        return None
    
    return {
        "identifier": identifier,
        "password": password
    }

@pytest.fixture(scope="function")
def artisan_auth_token(api_client, artisan_credentials):
    """Get artisan authentication token"""
    if not artisan_credentials:
        return None
    
    identifier = artisan_credentials["identifier"]
    password = artisan_credentials["password"]
    
    print(f"   Getting artisan token for: {identifier[:4]}****")
    
    login_data = {
        "identifier": identifier,
        "password": password
    }
    
    try:
        response = api_client.post("/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                # Try different possible token field names
                token = (
                    data.get("data", {}).get("access_token") or
                    data.get("data", {}).get("token") or
                    data.get("access_token") or
                    data.get("token")
                )
                if token:
                    print(f"   ✓ Artisan token obtained")
                    
                    # Check if it's really artisan (optional)
                    user_data = data.get("data", {}).get("user", {})
                    user_role = user_data.get("role", "").lower()
                    if "artisan" in user_role:
                        print(f"   ✓ User role: {user_role}")
                    else:
                        print(f"   ⚠ User role may not be artisan: {user_role}")
                    
                    return token
                else:
                    print(f"   ⚠ No token in response data")
            else:
                print(f"   ⚠ Login unsuccessful: {data.get('message')}")
        else:
            print(f"   ⚠ Login failed with status: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:200]}")
    
    except Exception as e:
        print(f"   ⚠ Error getting artisan token: {e}")
    
    return None