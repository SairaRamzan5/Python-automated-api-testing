import uuid
import random
import string
from datetime import datetime

def generate_unique_email(base_name="test"):
    """Generate a unique email for testing"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{base_name}_{timestamp}_{random_str}@test.com"

def generate_unique_phone():
    """Generate a unique phone number for testing"""
    # Generate random phone number (adjust based on your country code)
    random_number = ''.join(random.choices(string.digits, k=10))
    return f"+1{random_number}"

def get_test_cases_by_tag(tag, test_cases=None):
    """Get test cases by tag"""
    if test_cases is None:
        test_cases = ARTISAN_LOGIN_TEST_CASES
    return [tc for tc in test_cases if tag in tc.get("tags", [])]

# Artisan Login Test Cases
ARTISAN_LOGIN_TEST_CASES = [
    {
        "test_id": "TC_Artisan_Login_01",
        "description": "Approved artisan valid login with email",
        "data": {},  # Will be dynamically created
        "requires_approved_artisan": True,
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "success",
        "store_token": True
    },
    {
        "test_id": "TC_Artisan_Login_02",
        "description": "Approved artisan valid login with phone",
        "data": {},  # Will be dynamically created
        "requires_approved_artisan": True,
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "success",
        "store_token": True
    },
    {
        "test_id": "TC_Artisan_Login_03",
        "description": "Non-approved artisan login attempt",
        "data": {},  # Will be dynamically created
        "requires_non_approved_artisan": True,
        "expected_status": 400,  # Or 401/403 based on your API
        "expected_success": False,
        "expected_message": "phone not approved"
    },
    {
        "test_id": "TC_Artisan_Login_04",
        "description": "Artisan login with wrong password",
        "data": {
            "identifier": "approved_artisan@example.com",
            "password": "WrongPassword123!"
        },
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Invalid credentials"
    },
    {
        "test_id": "TC_Artisan_Login_05",
        "description": "Artisan login with non-existent email",
        "data": {
            "identifier": "nonexistent@example.com",
            "password": "SomePassword123!"
        },
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "User not found"
    },
    {
        "test_id": "TC_Artisan_Login_06",
        "description": "Artisan login with empty identifier",
        "data": {
            "identifier": "",
            "password": "SomePassword123!"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "identifier is required"
    },
    {
        "test_id": "TC_Artisan_Login_07",
        "description": "Artisan login with empty password",
        "data": {
            "identifier": "test@example.com",
            "password": ""
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "password is required"
    }
]

# Tags for filtering tests
ARTISAN_APPROVAL_TEST_CASES = [
    "TC_Artisan_Login_01",
    "TC_Artisan_Login_02",
    "TC_Artisan_Login_03"
]

def get_artisan_login_test_cases(tag=None):
    """Get artisan login test cases by tag"""
    if tag == "approval":
        return [tc for tc in ARTISAN_LOGIN_TEST_CASES if tc["test_id"] in ARTISAN_APPROVAL_TEST_CASES]
    return ARTISAN_LOGIN_TEST_CASES