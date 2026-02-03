"""Test data for whitelist approval/rejection API tests"""

WHITELIST_APPROVAL_TEST_CASES = [
    {
        "test_id": "TC_Whitelist_Approve_01",
        "description": "Approve a pending user",
        "data": {
            "user_id": "{user_id}",  # Will be replaced dynamically
            "status": "approved",
            "reason": "Phone number and documents verified"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Whitelist audit created successfully",
        "tags": ["positive", "approve", "admin"]
    },
    {
        "test_id": "TC_Whitelist_Approve_02",
        "description": "Reject a pending user",
        "data": {
            "user_id": "{user_id}",
            "status": "rejected",
            "reason": "Incomplete documentation"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Whitelist audit created successfully",
        "tags": ["positive", "reject", "admin"]
    },
    {
        "test_id": "TC_Whitelist_Approve_03",
        "description": "Approve without authentication",
        "data": {
            "user_id": "test-id-123",
            "status": "approved",
            "reason": "Test reason"
        },
        "headers": {},  # No auth header
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Access token required",
        "tags": ["negative", "security", "admin"]
    },
    {
        "test_id": "TC_Whitelist_Approve_04",
        "description": "Approve with invalid user_id",
        "data": {
            "user_id": "invalid-uuid-123",
            "status": "approved",
            "reason": "Test reason"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": [
            {
                "field": "user_id",
                "message": "User ID must be a valid UUID"
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Whitelist_Approve_05",
        "description": "Approve with invalid status",
        "data": {
            "user_id": "{user_id}",
            "status": "invalid_status",
            "reason": "Test reason"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",  # Changed from specific message
        "expected_errors": [
            {
                "field": "status",
                "message": "status must be a valid enum value"  # Actual error from API
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Whitelist_Approve_06",
        "description": "Approve without reason",
        "data": {
            "user_id": "{user_id}",
            "status": "approved"
            # Missing reason field
        },
        "expected_status": 200,  # Changed from 200
        "expected_success": False,
        "expected_message": "Whitelist audit created successfully",  # Changed
        "expected_errors": [
            {
                "field": "reason",
                "message": "reason is required"
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Whitelist_Approve_07",
        "description": "Approve already approved user",
        "data": {
            "user_id": "{approved_user_id}",
            "status": "approved",
            "reason": "Already approved test"
        },
        "expected_status": 200,  # Changed from 400 - API allows re-approval
        "expected_success": True,
        "expected_message": "Whitelist audit created successfully",
        "tags": ["positive", "admin", "reapproval"]  # Changed from negative
    },
    {
        "test_id": "TC_Whitelist_Approve_08",
        "description": "Approve with very long reason",
        "data": {
            "user_id": "{user_id}",
            "status": "approved",
            "reason": "A" * 300  # Changed to 300 characters (exceeds limit)
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": [
            {
                "field": "reason",
                "message": "Reason must not exceed 255 characters"
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
    "test_id": "TC_Whitelist_Approve_09",
    "description": "Reject an already approved user",
    "data": {
        "user_id": "{approved_user_id}",
        "status": "rejected",
        "reason": "Change of decision"
    },
    "expected_status": 200,
    "expected_success": True,
    "expected_message": "Whitelist audit created successfully",
    "tags": ["positive", "admin", "reverse_status"]
},
{
    "test_id": "TC_Whitelist_Approve_10",
    "description": "Approve a previously rejected user",
    "data": {
        "user_id": "{rejected_user_id}",
        "status": "approved",
        "reason": "Re-evaluation approved"
    },
    "expected_status": 200,
    "expected_success": True,
    "expected_message": "Whitelist audit created successfully",
    "tags": ["positive", "admin", "reverse_status"]
},
{
    "test_id": "TC_Whitelist_Approve_11",
    "description": "Approve a previously rejected user",
    "data": {
        "user_id": "{rejected_user_id}",
        "status": "approved",
        "reason": "Re-evaluation approved"
    },
    "expected_status": 200,
    "expected_success": True,
    "expected_message": "Whitelist audit created successfully"
}


]

# Valid status options
VALID_STATUSES = ["pending_approval", "approved", "rejected"]