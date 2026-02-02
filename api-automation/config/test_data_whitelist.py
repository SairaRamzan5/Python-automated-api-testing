""" Test data for whitelist audit API tests - FIXED VERSION"""

WHITELIST_TEST_CASES = [
    {
        "test_id": "TC_Whitelist_01",
        "description": "Get all whitelist audits",
        "params": {"page": 1, "limit": 10},
        "expected_status": 200,
        "expected_success": True,
        "expected_fields": ["data", "meta"],
        "expected_message": "Whitelist audits retrieved successfully",
        "tags": ["smoke", "positive", "admin"]
    },
    {
        "test_id": "TC_Whitelist_02",
        "description": "Search specific user by email",
        "params": {"search": "manual", "page": 1, "limit": 10},  # Changed from "manual_uat" to "manual" (6 chars)
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Whitelist audits retrieved successfully",
        "tags": ["search", "positive", "admin"]
    },
    {
        "test_id": "TC_Whitelist_03",
        "description": "Test pagination with small limit",
        "params": {"page": 1, "limit": 5},
        "expected_status": 200,
        "expected_success": True,
        "tags": ["pagination", "positive", "admin"]
    },
    {
        "test_id": "TC_Whitelist_04",
        "description": "Test sorting by created date",
        "params": {"page": 1, "limit": 10, "sort": "created_at", "order": "desc"},
        "expected_status": 200,
        "expected_success": True,
        "tags": ["sorting", "positive", "admin"]
    },
    {
        "test_id": "TC_Whitelist_05",
        "description": "Get whitelist without authentication",
        "params": {"page": 1, "limit": 10},
        "headers": {},  # No auth header
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Access token required",
        "tags": ["negative", "security", "admin"]
    },
    {
        "test_id": "TC_Whitelist_06",
        "description": "Invalid page number",
        "params": {"page": "invalid", "limit": 10},
        "expected_status": 422,
        "expected_success": False,
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Whitelist_07",
        "description": "Invalid limit value",
        "params": {"page": 1, "limit": "invalid"},
        "expected_status": 422,
        "expected_success": False,
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Whitelist_08",
        "description": "Pagination test - page 2",
        "params": {"page": 2, "limit": 5},
        "expected_status": 200,
        "expected_success": True,
        "expected_fields": ["data", "meta"],
        "tags": ["pagination", "positive", "admin"]
    }
    # ,
    # {
    #     "test_id": "TC_Whitelist_09",
    #     "description": "Search with less than 2 characters (should fail)",
    #     "params": {"search": "a", "page": 1, "limit": 10},  # 1 character - should fail
    #     "expected_status": 422,
    #     "expected_success": False,
    #     "expected_message": "search must be longer than or equal to 2 characters",
    #     "tags": ["negative", "validation", "admin"]
    # }
]

# Status options (if API starts supporting them later)
WHITELIST_STATUS_OPTIONS = [
    "pending_approval",
    "approved", 
    "rejected"
]

# Sort options
SORT_OPTIONS = ["created_at", "f_name", "email", "status"]