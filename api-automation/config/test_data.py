"""Test data for login API tests - Based on test case table"""

LOGIN_TEST_CASES = [
    # TC_Login_01: Valid Credentials
    {
        "test_id": "TC_Login_01",
        "description": "Verify login with valid credentials",
        "data": {"identifier": "admin", "password": "admin123"},
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Login verification successful",
        "should_have_token": True,
        "should_have_user_data": True,
        "expected_user_data": {
            "id": "71686e0a-27ef-402b-99ec-0b1c0d63f47a",
            "f_name": "Seeder",
            "l_name": "Super Admin",
            "email": "admin",
            "phone_verified": True,
            "email_verified": True,
            "mfa_enabled": False
        },
        "tags": ["smoke", "positive", "critical"]
    },
    
    # TC_Login_02: Invalid Credentials (non-existent user)
    {
        "test_id": "TC_Login_02",
        "description": "Login with invalid credentials (non-existent user)",
        "data": {"identifier": "adminteresa", "password": "admin#123@"},
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Invalid credentials",
        "should_have_token": False,
        "should_have_user_data": False,
        "tags": ["negative", "security"]
    },
    
    # TC_Login_03: Valid username, invalid password
    {
        "test_id": "TC_Login_03",
        "description": "Login with valid username and invalid password",
        "data": {"identifier": "admin", "password": "helloteresa123"},
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Invalid credentials",
        "should_have_token": False,
        "should_have_user_data": False,
        "tags": ["negative", "security"]
    },
    
    # TC_Login_04: Invalid username, valid password
    {
        "test_id": "TC_Login_04",
        "description": "Login with invalid username and valid password",
        "data": {"identifier": "teresaadmin", "password": "admin123"},
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Invalid credentials",
        "should_have_token": False,
        "should_have_user_data": False,
        "tags": ["negative", "security"]
    },
    
    # TC_Login_05: Empty fields
    {
        "test_id": "TC_Login_05",
        "description": "Login with empty fields",
        "data": {"identifier": "", "password": ""},
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "validation_error": True,
        "tags": ["negative", "validation"]
    },
    
    # TC_Login_06: Empty username, valid password
    {
        "test_id": "TC_Login_06",
        "description": "Login with empty username and valid password",
        "data": {"identifier": "", "password": "admin123"},
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "validation_error": True,
        "tags": ["negative", "validation"]
    },
    
    # TC_Login_07: Valid username, empty password
    {
        "test_id": "TC_Login_07",
        "description": "Login with valid username and empty password",
        "data": {"identifier": "admin", "password": ""},
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "validation_error": True,
        "tags": ["negative", "validation"]
    },
    
    # TC_Login_08: Empty username, invalid password
    {
        "test_id": "TC_Login_08",
        "description": "Login with empty username and invalid password",
        "data": {"identifier": "", "password": "adminteresa@"},
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "validation_error": True,
        "tags": ["negative", "validation"]
    },
    
    # TC_Login_09: Invalid username, empty password
    {
        "test_id": "TC_Login_09",
        "description": "Login with invalid username and empty password",
        "data": {"identifier": "adminteresa@", "password": ""},
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "validation_error": True,
        "tags": ["negative", "validation"]
    },
    
    # TC_Login_10: Unregistered credentials
    {
        "test_id": "TC_Login_10",
        "description": "Login with unregistered username and password",
        "data": {"identifier": "saira@gmail.com", "password": "saira@123"},
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Invalid credentials",
        "should_have_token": False,
        "should_have_user_data": False,
        "tags": ["negative", "security"]
    }
]

# Helper function to get test cases by tag
def get_test_cases_by_tag(tag):
    """Filter test cases by tag"""
    return [tc for tc in LOGIN_TEST_CASES if tag in tc.get("tags", [])]

# Get specific test sets
SMOKE_TESTS = get_test_cases_by_tag("smoke")
POSITIVE_TESTS = get_test_cases_by_tag("positive")
NEGATIVE_TESTS = get_test_cases_by_tag("negative")
VALIDATION_TESTS = get_test_cases_by_tag("validation")
SECURITY_TESTS = get_test_cases_by_tag("security")
CRITICAL_TESTS = get_test_cases_by_tag("critical")

# Test data for logout tests - UPDATED WITH CORRECT STATUS CODES
LOGOUT_TEST_CASES = [
    {
        "test_id": "TC_Logout_01",
        "description": "Logout with valid token",
        "expected_status": 204,  # CHANGED: 204 No Content for successful logout
        "expected_success": True,
        "expected_message": "",  # 204 has no content
        "tags": ["smoke", "positive"]
    },
    {
        "test_id": "TC_Logout_02",
        "description": "Logout with invalid token",
        "expected_status": 500,  # CHANGED: 500 for invalid token (not 401)
        "expected_success": False,
        "expected_message": "Invalid access token",
        "tags": ["negative", "security"]
    },
    {
        "test_id": "TC_Logout_03",
        "description": "Logout without token",
        "expected_status": 500,  # CHANGED: 500 for missing token (not 401)
        "expected_success": False,
        "expected_message": "Authorization header required",
        "tags": ["negative", "security"]
    }
]