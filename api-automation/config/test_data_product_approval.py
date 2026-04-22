"""Test data for product approval/rejection API tests"""

PRODUCT_APPROVAL_TEST_CASES = [
    # ── Positive Cases ─────────────────────────────────────────────────────────
    {
        "test_id": "TC_Product_Approve_01",
        "description": "Approve a pending product",
        "data": {
            "product_id": "{product_id}",
            "status": "approved",
            "reason": "Product details, pricing, and images verified"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product approved successfully",
        "tags": ["positive", "approve", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_02",
        "description": "Reject a pending product",
        "data": {
            "product_id": "{product_id}",
            "status": "rejected",
            "reason": "Images do not meet quality standards"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product rejected successfully",
        "tags": ["positive", "reject", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_03",
        "description": "Approve product without authentication",
        "data": {
            "product_id": "{product_id}",
            "status": "approved",
            "reason": "Test reason"
        },
        "headers": {},   # No auth header — cleared in test logic
        "expected_status": 401,
        "expected_success": False,
        "expected_message": "Access token required",
        "tags": ["negative", "security", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_04",
        "description": "Approve with invalid product_id (non-UUID)",
        "data": {
            "product_id": "invalid-uuid-123",
            "status": "approved",
            "reason": "Test reason"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": [
            {
                "field": "product_id",
                "message": "Product ID must be a valid UUID"
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_05",
        "description": "Approve with non-existent product_id (valid UUID format)",
        "data": {
            "product_id": "00000000-0000-0000-0000-000000000000",
            "status": "approved",
            "reason": "Test reason"
        },
        "expected_status": 404,
        "expected_success": False,
        "expected_message": "Product not found",
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_06",
        "description": "Approve with invalid status value",
        "data": {
            "product_id": "{product_id}",
            "status": "invalid_status",
            "reason": "Test reason"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": [
            {
                "field": "status",
                "message": "status must be a valid enum value"
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_07",
        "description": "Approve without providing reason (reason is optional)",
        "data": {
            "product_id": "{product_id}",
            "status": "approved"
            # reason intentionally omitted
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product approved successfully",
        "tags": ["positive", "validation", "admin", "optional_field"]
    },
    {
        "test_id": "TC_Product_Approve_08",
        "description": "Approve with empty reason string (should be rejected)",
        "data": {
            "product_id": "{product_id}",
            "status": "approved",
            "reason": ""
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": [
            {
                "field": "reason",
                "message": "Reason cannot be empty if provided"
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_09",
        "description": "Approve with whitespace-only reason (BUG: Currently accepted)",
        "data": {
            "product_id": "{product_id}",
            "status": "approved",
            "reason": "   "    # Whitespace only — CURRENTLY ACCEPTED (BUG)
        },
        "expected_status": 200,   # Reflects actual API behaviour; should be 422
        "expected_success": True,
        "expected_message": "Product approved successfully",
        "expected_errors": [],
        "is_bug": True,
        "tags": ["negative", "validation", "admin", "bug"]
    },
    {
        "test_id": "TC_Product_Approve_10",
        "description": "Approve with reason exceeding maximum length (>255 chars)",
        "data": {
            "product_id": "{product_id}",
            "status": "approved",
            "reason": "A" * 300
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
        "test_id": "TC_Product_Approve_11",
        "description": "Approve with single-character reason (minimum valid length)",
        "data": {
            "product_id": "{product_id}",
            "status": "approved",
            "reason": "a"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product approved successfully",
        "tags": ["positive", "validation", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_12",
        "description": "Approve with reason at exact maximum length (255 chars)",
        "data": {
            "product_id": "{product_id}",
            "status": "approved",
            "reason": "B" * 255
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product approved successfully",
        "tags": ["positive", "boundary", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_13",
        "description": "Re-approve an already approved product",
        "data": {
            "product_id": "{approved_product_id}",
            "status": "approved",
            "reason": "Re-approval after further review"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product approved successfully",
        "tags": ["positive", "admin", "reapproval"]
    },
    {
        "test_id": "TC_Product_Approve_14",
        "description": "Reject an already approved product (status reversal)",
        "data": {
            "product_id": "{approved_product_id}",
            "status": "rejected",
            "reason": "Policy violation found after initial approval"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product rejected successfully",
        "tags": ["positive", "admin", "reverse_status"]
    },
    {
        "test_id": "TC_Product_Approve_15",
        "description": "Approve a previously rejected product",
        "data": {
            "product_id": "{rejected_product_id}",
            "status": "approved",
            "reason": "Re-evaluated and now meets all requirements"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product approved successfully",
        "tags": ["positive", "admin", "reverse_status"]
    },
    {
        "test_id": "TC_Product_Approve_16",
        "description": "Reject with single-character reason",
        "data": {
            "product_id": "{product_id}",
            "status": "rejected",
            "reason": "X"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product rejected successfully",
        "tags": ["positive", "validation", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_17",
        "description": "Approve with missing product_id field",
        "data": {
            "status": "approved",
            "reason": "Test reason"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": [
            {
                "field": "product_id",
                "message": "product_id is required"
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_18",
        "description": "Approve with missing status field",
        "data": {
            "product_id": "{product_id}",
            "reason": "Test reason"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": [
            {
                "field": "status",
                "message": "status is required"
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_19",
        "description": "Approve with empty product_id string",
        "data": {
            "product_id": "",
            "status": "approved",
            "reason": "Test reason"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": [
            {
                "field": "product_id",
                "message": "product_id must not be empty"
            }
        ],
        "tags": ["negative", "validation", "admin"]
    },
    {
        "test_id": "TC_Product_Approve_20",
        "description": "Approve with special characters in reason",
        "data": {
            "product_id": "{product_id}",
            "status": "approved",
            "reason": "Verified: price ✓, images ✓, description ✓ — all good!"
        },
        "expected_status": 200,
        "expected_success": True,
        "expected_message": "Product approved successfully",
        "tags": ["positive", "validation", "admin"]
    },
]

# Valid status options for product approval
VALID_PRODUCT_STATUSES = ["pending_approval", "approved", "rejected"]