# """Simple pytest configuration - MINIMAL VERSION"""

# import pytest
# import time
# import sys
# import os

# # Add the project root to Python path
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# @pytest.fixture(scope="function")
# def api_client():
#     """Fixture to provide API client instance for UAT"""
#     from api.client import APIClient
#     from config.settings import settings
    
#     client = APIClient(base_url=settings.BASE_URL)
    
#     yield client
    
#     # Cleanup after test
#     client.clear_auth_token()

# @pytest.fixture(scope="session", autouse=True)
# def session_setup():
#     """Session setup - runs once at the start"""
#     from config.settings import settings
    
#     print(f"\n{'='*80}")
#     print(f"Starting UAT Test Session")
#     print(f"Environment: {settings.ENVIRONMENT}")
#     print(f"Base URL: {settings.BASE_URL}")
#     print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
#     print(f"{'='*80}")
    
#     yield
    
#     print(f"\n{'='*80}")
#     print(f"Test Session Complete")
#     print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
#     print(f"{'='*80}")

# @pytest.fixture(autouse=True)
# def test_delay():
#     """Add small delay between tests to prevent rate limiting"""
#     yield
#     from config.settings import settings
#     time.sleep(settings.TEST_DELAY)

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

@pytest.fixture
def admin_auth_token(api_client):
    """Get admin authentication token - NEW FIXTURE ADDED HERE"""
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
    time.sleep(settings.TEST_DELAY)