# """ Test data for whitelist audit API tests - FIXED VERSION"""

# WHITELIST_TEST_CASES = [
#     {
#         "test_id": "TC_Whitelist_01",
#         "description": "Get all whitelist audits",
#         "params": {"page": 1, "limit": 10},
#         "expected_status": 200,
#         "expected_success": True,
#         "expected_fields": ["data", "meta"],
#         "expected_message": "Whitelist audits retrieved successfully",
#         "tags": ["smoke", "positive", "admin"]
#     },
#     {
#         "test_id": "TC_Whitelist_02",
#         "description": "Search specific user by email",
#         "params": {"search": "manual", "page": 1, "limit": 10},  # Changed from "manual_uat" to "manual" (6 chars)
#         "expected_status": 200,
#         "expected_success": True,
#         "expected_message": "Whitelist audits retrieved successfully",
#         "tags": ["search", "positive", "admin"]
#     },
#     {
#         "test_id": "TC_Whitelist_03",
#         "description": "Test pagination with small limit",
#         "params": {"page": 1, "limit": 5},
#         "expected_status": 200,
#         "expected_success": True,
#         "tags": ["pagination", "positive", "admin"]
#     },
#     {
#         "test_id": "TC_Whitelist_04",
#         "description": "Test sorting by created date",
#         "params": {"page": 1, "limit": 10, "sort": "created_at", "order": "desc"},
#         "expected_status": 200,
#         "expected_success": True,
#         "tags": ["sorting", "positive", "admin"]
#     },
#     {
#         "test_id": "TC_Whitelist_05",
#         "description": "Get whitelist without authentication",
#         "params": {"page": 1, "limit": 10},
#         "headers": {},  # No auth header
#         "expected_status": 401,
#         "expected_success": False,
#         "expected_message": "Access token required",
#         "tags": ["negative", "security", "admin"]
#     },
#     {
#         "test_id": "TC_Whitelist_06",
#         "description": "Invalid page number",
#         "params": {"page": "invalid", "limit": 10},
#         "expected_status": 422,
#         "expected_success": False,
#         "tags": ["negative", "validation", "admin"]
#     },
#     {
#         "test_id": "TC_Whitelist_07",
#         "description": "Invalid limit value",
#         "params": {"page": 1, "limit": "invalid"},
#         "expected_status": 422,
#         "expected_success": False,
#         "tags": ["negative", "validation", "admin"]
#     },
#     {
#         "test_id": "TC_Whitelist_08",
#         "description": "Pagination test - page 2",
#         "params": {"page": 2, "limit": 5},
#         "expected_status": 200,
#         "expected_success": True,
#         "expected_fields": ["data", "meta"],
#         "tags": ["pagination", "positive", "admin"]
#     }
#     # ,
#     # {
#     #     "test_id": "TC_Whitelist_09",
#     #     "description": "Search with less than 2 characters (should fail)",
#     #     "params": {"search": "a", "page": 1, "limit": 10},  # 1 character - should fail
#     #     "expected_status": 422,
#     #     "expected_success": False,
#     #     "expected_message": "search must be longer than or equal to 2 characters",
#     #     "tags": ["negative", "validation", "admin"]
#     # }
# ]

# # Status options (if API starts supporting them later)
# WHITELIST_STATUS_OPTIONS = [
#     "pending_approval",
#     "approved", 
#     "rejected"
# ]

# # Sort options
# SORT_OPTIONS = ["created_at", "f_name", "email", "status"]

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
        "params": {"search": "manual", "page": 1, "limit": 10},
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
    # SORTING TESTS - UPDATED
    {
        "test_id": "TC_Whitelist_04",
        "description": "Test sorting by created date (descending)",
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
    },
    # ADDITIONAL SORTING TESTS
    {
        "test_id": "TC_Whitelist_09",
        "description": "Test sorting by username (f_name) ascending",
        "params": {"page": 1, "limit": 10, "sort": "f_name", "order": "asc"},
        "expected_status": 200,
        "expected_success": True,
        "tags": ["sorting", "positive", "admin"]
    },
    {
        "test_id": "TC_Whitelist_10",
        "description": "Test sorting by username (f_name) descending",
        "params": {"page": 1, "limit": 10, "sort": "f_name", "order": "desc"},
        "expected_status": 200,
        "expected_success": True,
        "tags": ["sorting", "positive", "admin"]
    },
    {
        "test_id": "TC_Whitelist_11",
        "description": "Test sorting by status ascending",
        "params": {"page": 1, "limit": 10, "sort": "status", "order": "asc"},
        "expected_status": 200,
        "expected_success": True,
        "tags": ["sorting", "positive", "admin"]
    },
    {
        "test_id": "TC_Whitelist_12",
        "description": "Test sorting by status descending",
        "params": {"page": 1, "limit": 10, "sort": "status", "order": "desc"},
        "expected_status": 200,
        "expected_success": True,
        "tags": ["sorting", "positive", "admin"]
    },
    {
        "test_id": "TC_Whitelist_13",
        "description": "Test sorting by email ascending",
        "params": {"page": 1, "limit": 10, "sort": "email", "order": "asc"},
        "expected_status": 200,
        "expected_success": True,
        "tags": ["sorting", "positive", "admin"]
    },
    # ADDITIONAL SEARCH TESTS
    {
        "test_id": "TC_Whitelist_14",
        "description": "Search by partial phone number",
        "params": {"search": "+880", "page": 1, "limit": 10},
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Whitelist audits retrieved successfully",
        "tags": ["search", "positive", "admin"]
    },
    {
        "test_id": "TC_Whitelist_15",
        "description": "Search by partial name",
        "params": {"search": "Test", "page": 1, "limit": 10},
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Whitelist audits retrieved successfully",
        "tags": ["search", "positive", "admin"]
    }
]

# Status options (if API starts supporting them later)
WHITELIST_STATUS_OPTIONS = [
    "pending_approval",
    "approved", 
    "rejected"
]

# Sort options - UPDATED
SORT_OPTIONS = ["created_at", "f_name", "email", "status", "l_name", "phone", "updated_at"]

# Order options
ORDER_OPTIONS = ["asc", "desc"]