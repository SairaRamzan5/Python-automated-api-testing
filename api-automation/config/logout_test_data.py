# config/test_data_logout.py
"""Test data for logout API tests"""

LOGOUT_TEST_CASES = [
    {
        "test_id": "TC_Logout_01",
        "description": "Logout with valid token",
        "headers": {"Authorization": "Bearer {token}"},
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Logged out successfully",
        "tags": ["smoke", "positive"]
    },
    {
        "test_id": "TC_Logout_02",
        "description": "Logout without token",
        "headers": {},
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Unauthorized",
        "tags": ["negative", "security"]
    },
    {
        "test_id": "TC_Logout_03",
        "description": "Logout with invalid token",
        "headers": {"Authorization": "Bearer invalid_token_123"},
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Invalid token",
        "tags": ["negative", "security"]
    },
    {
        "test_id": "TC_Logout_04",
        "description": "Logout with expired token",
        "headers": {"Authorization": "Bearer expired_token_xyz"},
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Token expired",
        "tags": ["negative", "security"]
    },
    {
        "test_id": "TC_Logout_05",
        "description": "Logout with malformed token",
        "headers": {"Authorization": "InvalidFormat"},
        "expected_status": 400,
        "expected_success": False,
        "expected_message": "Invalid authorization format",
        "tags": ["negative", "validation"]
    },
    {
        "test_id": "TC_Logout_06",
        "description": "Logout twice with same token",
        "headers": {"Authorization": "Bearer {token}"},
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Token already invalidated",
        "tags": ["negative", "security"]
    }
]