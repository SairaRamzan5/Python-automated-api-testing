"""Test data for Techniques Get API tests - WITH BUG DOCUMENTATION"""

TECHNIQUES_GET_TEST_DATA = {
    # ==================== POSITIVE TEST CASES ====================
    "positive_cases": [
        {
            "test_id": "TC_TG_01",
            "description": "Get all active techniques with default pagination",
            "params": {
                "is_active": "true"
            },
            "expected_status": 200,
            "expected_success": True,
            "expected_fields": ["data", "meta"],
            "pagination_expected": True,
            "pagination_location": "meta.pagination",
            "min_data_count": 1,
            "tags": ["positive", "smoke", "pagination"],
            "priority": "high"
        },
        {
            "test_id": "TC_TG_02",
            "description": "Get all techniques (active and inactive)",
            "params": {},
            "expected_status": 200,
            "expected_success": True,
            "expected_fields": ["data", "meta"],
            "pagination_expected": True,
            "pagination_location": "meta.pagination",
            "tags": ["positive", "all_techniques"],
            "priority": "medium"
        },
        {
            "test_id": "TC_TG_03",
            "description": "Get techniques with pagination - page 1, limit 5",
            "params": {
                "page": "1",
                "limit": "5"
            },
            "expected_status": 200,
            "expected_success": True,
            "pagination_expected": True,
            "pagination_location": "meta.pagination",
            "expected_pagination_fields": ["page", "limit", "total", "total_pages", "has_next", "has_prev"],
            "max_data_count": 5,
            "tags": ["positive", "pagination"],
            "priority": "high"
        },
        # NOTE: Search tests will FAIL due to API bug
        {
            "test_id": "TC_TG_04",
            "description": "BUG: Search should return ONLY 'Single' techniques",
            "params": {
                "search": "Single"
            },
            "expected_status": 200,
            "expected_success": True,
            "expected_data_count": 0,  # Should be 1, but returns ALL due to bug
            "bug_note": "API BUG: Returns ALL techniques instead of filtered",
            "tags": ["positive", "search", "bug"],
            "priority": "high"
        },
        {
            "test_id": "TC_TG_05",
            "description": "BUG: Search should return ONLY 'Test' techniques",
            "params": {
                "search": "Test"
            },
            "expected_status": 200,
            "expected_success": True,
            "expected_data_count": 2,  # Should be 2, but returns ALL due to bug
            "bug_note": "API BUG: Returns ALL techniques instead of filtered",
            "tags": ["positive", "search", "bug"],
            "priority": "high"
        },
        {
            "test_id": "TC_TG_06",
            "description": "Get techniques sorted by name ascending",
            "params": {
                "sort": "name",
                "order": "asc"
            },
            "expected_status": 200,
            "expected_success": True,
            "sort_validation_required": True,
            "sort_field": "name",
            "sort_order": "asc",
            "tags": ["positive", "sorting"],
            "priority": "medium"
        },
        {
            "test_id": "TC_TG_07",
            "description": "Get techniques sorted by created_at descending",
            "params": {
                "sort": "created_at",
                "order": "desc"
            },
            "expected_status": 200,
            "expected_success": True,
            "sort_validation_required": True,
            "sort_field": "created_at",
            "sort_order": "desc",
            "tags": ["positive", "sorting"],
            "priority": "medium"
        },
        {
            "test_id": "TC_TG_08",
            "description": "Get inactive techniques only",
            "params": {
                "is_active": "false"
            },
            "expected_status": 200,
            "expected_success": True,
            "expected_data_count": 0,  # All are active
            "tags": ["positive", "inactive"],
            "priority": "low"
        },
        {
            "test_id": "TC_TG_09",
            "description": "Search with active filter",
            "params": {
                "is_active": "true",
                "search": "Single"
            },
            "expected_status": 200,
            "expected_success": True,
            "expected_data_count": 1,  # Should be 1, but bug returns ALL
            "bug_note": "API BUG: Search parameter ignored",
            "tags": ["positive", "combined_filters", "bug"],
            "priority": "medium"
        },
    ],
    
    # ==================== NEGATIVE TEST CASES ====================
    "negative_cases": [
        {
            "test_id": "TC_TG_10",
            "description": "Get techniques without authentication",
            "params": {},
            "headers": {},
            "expected_status": 401,
            "expected_success": False,
            "expected_message": "Access token required",
            "tags": ["negative", "security", "authentication"],
            "priority": "high"
        },
        {
            "test_id": "TC_TG_11",
            "description": "BUG: Search non-existent should return empty",
            "params": {
                "search": "NONEXISTENT_TECHNIQUE_XYZ123"
            },
            "expected_status": 200,
            "expected_success": True,
            "expected_data_count": 0,  # Should be 0, but bug returns ALL
            "bug_note": "API BUG: Returns ALL techniques for non-existent search",
            "tags": ["negative", "search", "bug"],
            "priority": "high"
        },
        {
            "test_id": "TC_TG_12",
            "description": "Search with special characters",
            "params": {
                "search": "@#$%^&*()"
            },
            "expected_status": 200,
            "expected_success": True,
            "expected_data_count": 0,  # Should be 0, but bug returns ALL
            "bug_note": "API BUG: Returns ALL techniques",
            "tags": ["negative", "search", "bug"],
            "priority": "low"
        },
        {
            "test_id": "TC_TG_13",
            "description": "Search with very long string",
            "params": {
                "search": "a" * 100
            },
            "expected_status": 200,
            "expected_success": True,
            "expected_data_count": 0,  # Should be 0, but bug returns ALL
            "bug_note": "API BUG: Returns ALL techniques",
            "tags": ["negative", "search", "bug"],
            "priority": "low"
        },
        {
            "test_id": "TC_TG_14",
            "description": "Search case sensitivity test",
            "params": {
                "search": "SINGLE"  # UPPERCASE
            },
            "expected_status": 200,
            "expected_success": True,
            "expected_data_count": 1,  # Should be 1 if case-insensitive, bug returns ALL
            "bug_note": "API BUG: Returns ALL techniques",
            "tags": ["negative", "search", "case", "bug"],
            "priority": "low"
        },
    ],
    
    # ==================== BUG VERIFICATION CASES ====================
    "bug_cases": [
        {
            "test_id": "TC_BUG_01",
            "description": "CRITICAL BUG: Search parameter is IGNORED",
            "params": {
                "search": "Single"
            },
            "expected_status": 200,
            "expected_success": True,
            "bug_verification": True,
            "expected_behavior": "Should return ONLY techniques containing 'Single'",
            "actual_behavior": "Returns ALL techniques (BUG)",
            "severity": "Critical",
            "tags": ["bug", "critical", "search"],
            "priority": "critical"
        },
        {
            "test_id": "TC_BUG_02",
            "description": "CRITICAL BUG: Non-existent search returns ALL techniques",
            "params": {
                "search": "DELETED_NONEXISTENT_123"
            },
            "expected_status": 200,
            "expected_success": True,
            "bug_verification": True,
            "expected_behavior": "Should return EMPTY array",
            "actual_behavior": "Returns ALL techniques (BUG)",
            "severity": "Critical",
            "tags": ["bug", "critical", "search"],
            "priority": "critical"
        },
        {
            "test_id": "TC_BUG_03",
            "description": "BUG: Search returns same count as no search",
            "params": {
                "search": "Test"
            },
            "expected_status": 200,
            "expected_success": True,
            "bug_verification": True,
            "test_method": "Compare with no-search request",
            "expected": "Different result count",
            "actual": "Same result count (BUG)",
            "severity": "High",
            "tags": ["bug", "search", "verification"],
            "priority": "high"
        },
    ]
}

# Configuration
ACTUAL_TECHNIQUE_FIELDS = ["id", "name", "parent_name", "is_active", "values", "children"]
OPTIONAL_TECHNIQUE_FIELDS = ["description", "created_at", "updated_at", "is_duplicate"]

VALID_SORT_FIELDS = ["name", "created_at", "updated_at", "is_active"]
VALID_ORDER_VALUES = ["asc", "desc"]
DEFAULT_PAGE = 1
DEFAULT_LIMIT = 15
MAX_LIMIT = 100

TEST_CONFIG = {
    "max_limit": 100,
    "default_limit": 15,
    "default_page": 1,
    "valid_sort_fields": ["name", "created_at", "updated_at", "is_active"],
    "valid_order_values": ["asc", "desc"],
    "valid_boolean_values": ["true", "false", "1", "0"],
    "pagination_location": "meta.pagination",
    "required_technique_fields": ["id", "name", "is_active", "values"],
    "search_fields": ["name"],
    "max_search_length": 50,
    "technique_count": 3  # Based on your data
}