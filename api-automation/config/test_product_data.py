"""Test data for Product Creation API tests"""

import time
from datetime import datetime

class ProductTestData:
    """Test data configuration for product creation tests"""
    
    # Valid test data from your reference
    VALID_PRODUCT = {
        "name": "Handwritten notes",
        "description": "You can give your own designs or pinterest styles and we will print them for you",
        "hours_to_make": 1,
        "monthly_qty": 300,
        "annual_qty": 2000,
        "custom_price": 20,
        "is_active": False,
        "status": "pending",
        "workshops": [],
        "materials": [
            {
                "name": "ink",
                "price": 150,
                "quantity": 6,
                "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
            },
            {
                "name": "paper",
                "price": 10,
                "quantity": 5,
                "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
            }
        ],
        "techniques": [
            {
                "id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849"
            }
        ],
        "files": [
            {
                "id": "58a82002-020b-4e12-917f-5fcb3dccd29d"
            }
        ]
    }
    
    # Alternative file IDs from your response
    ALTERNATIVE_FILE_IDS = [
        "58a82002-020b-4e12-917f-5fcb3dccd29d",
        "78bbd7e5-c036-4544-aea6-0013838946cb",
        "1faa4719-74f3-4e08-9ba4-741d40e70aba",
        "9f990a97-ccc9-43b8-b877-9668557f06f3",
        "b13e6538-45cb-4424-b7ff-a8c76001a39d"
    ]
    
    # Additional materials for testing
    ADDITIONAL_MATERIALS = [
        {
            "name": "fabric",
            "price": 200,
            "quantity": 2,
            "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
        },
        {
            "name": "thread",
            "price": 50,
            "quantity": 10,
            "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
        },
        {
            "name": "paint",
            "price": 80,
            "quantity": 3,
            "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
        }
    ]
    
    # Different status values
    STATUS_VALUES = ["pending", "draft", "active", "inactive", "rejected"]
    
    @staticmethod
    def generate_unique_product_name(base_name="Handwritten notes"):
        """Generate a unique product name with timestamp"""
        timestamp = int(time.time())
        return f"{base_name} - {timestamp}"
    
    @staticmethod
    def get_valid_product_payload(**kwargs):
        """Get a valid product payload with optional overrides"""
        payload = ProductTestData.VALID_PRODUCT.copy()
        
        # Make name unique by default
        if "name" not in kwargs:
            payload["name"] = ProductTestData.generate_unique_product_name()
        
        # Update with any provided kwargs
        payload.update(kwargs)
        return payload
    
    # Test cases for validation
    VALIDATION_TEST_CASES = [
        {
            "test_id": "TC-001",
            "name": "Create product with valid data",
            "payload": {},
            "expected_status": 201,
            "expected_fields": ["id", "name", "status", "techniques", "materials"],
            "description": "Should create product successfully with all required fields"
        },
        {
            "test_id": "TC-002",
            "name": "Create product with multiple files",
            "payload": {
                "files": [
                    {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"},
                    {"id": "78bbd7e5-c036-4544-aea6-0013838946cb"}
                ]
            },
            "expected_status": 201,
            "expected_fields": ["id", "files"],
            "description": "Should accept product with multiple file references"
        },
        {
            "test_id": "TC-003",
            "name": "Create product with additional materials",
            "payload": {
                "materials": [
                    {
                        "name": "ink",
                        "price": 150,
                        "quantity": 6,
                        "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
                    },
                    {
                        "name": "paper",
                        "price": 10,
                        "quantity": 5,
                        "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
                    },
                    {
                        "name": "fabric",
                        "price": 200,
                        "quantity": 2,
                        "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
                    }
                ]
            },
            "expected_status": 201,
            "expected_fields": ["id", "materials"],
            "description": "Should accept product with multiple materials"
        },
        {
            "test_id": "TC-004",
            "name": "Create product with active status",
            "payload": {
                "status": "active",
                "is_active": True
            },
            "expected_status": 201,
            "expected_fields": ["id", "status", "is_active"],
            "description": "Should accept product with active status"
        },
        {
            "test_id": "TC-005",
            "name": "Create product with high quantities",
            "payload": {
                "monthly_qty": 1000,
                "annual_qty": 12000,
                "custom_price": 99.99
            },
            "expected_status": 201,
            "expected_fields": ["id", "monthly_qty", "annual_qty", "custom_price"],
            "description": "Should accept product with high values"
        }
    ]
    
    # Negative test cases
    NEGATIVE_TEST_CASES = [
        {
            "test_id": "TC-101",
            "name": "Missing required name field",
            "payload": {"name": None},
            "expected_status": 422,
            "expected_error": "name",
            "description": "Should reject product without name"
        },
        {
            "test_id": "TC-102",
            "name": "Empty name field",
            "payload": {"name": ""},
            "expected_status": 422,
            "expected_error": "name",
            "description": "Should reject product with empty name"
        },
        {
            "test_id": "TC-103",
            "name": "Missing description",
            "payload": {"description": None},
            "expected_status": 422,
            "expected_error": "description",
            "description": "Should reject product without description"
        },
        {
            "test_id": "TC-104",
            "name": "Negative hours to make",
            "payload": {"hours_to_make": -1},
            "expected_status": 422,
            "expected_error": "hours_to_make",
            "description": "Should reject negative hours"
        },
        {
            "test_id": "TC-105",
            "name": "Zero hours to make",
            "payload": {"hours_to_make": 0},
            "expected_status": 422,
            "expected_error": "hours_to_make",
            "description": "Should reject zero hours"
        },
        {
            "test_id": "TC-106",
            "name": "Negative monthly quantity",
            "payload": {"monthly_qty": -10},
            "expected_status": 422,
            "expected_error": "monthly_qty",
            "description": "Should reject negative monthly quantity"
        },
        {
            "test_id": "TC-107",
            "name": "Negative annual quantity",
            "payload": {"annual_qty": -100},
            "expected_status": 422,
            "expected_error": "annual_qty",
            "description": "Should reject negative annual quantity"
        },
        {
            "test_id": "TC-108",
            "name": "Annual less than monthly quantity",
            "payload": {"annual_qty": 100, "monthly_qty": 200},
            "expected_status": 422,
            "expected_error": "annual_qty",
            "description": "Should reject annual less than monthly"
        },
        {
            "test_id": "TC-109",
            "name": "Negative custom price",
            "payload": {"custom_price": -5},
            "expected_status": 422,
            "expected_error": "custom_price",
            "description": "Should reject negative price"
        },
        {
            "test_id": "TC-110",
            "name": "Invalid technique ID format",
            "payload": {"techniques": [{"id": "invalid-id"}]},
            "expected_status": 422,
            "expected_error": "techniques",
            "description": "Should reject invalid technique ID"
        },
        {
            "test_id": "TC-111",
            "name": "Invalid file ID format",
            "payload": {"files": [{"id": "invalid-file"}]},
            "expected_status": 422,
            "expected_error": "files",
            "description": "Should reject invalid file ID"
        },
        {
            "test_id": "TC-112",
            "name": "Empty materials array",
            "payload": {"materials": []},
            "expected_status": 422,
            "expected_error": "materials",
            "description": "Should reject empty materials"
        },
        {
            "test_id": "TC-113",
            "name": "Empty techniques array",
            "payload": {"techniques": []},
            "expected_status": 422,
            "expected_error": "techniques",
            "description": "Should reject empty techniques"
        }
    ]
    
    # Material validation test cases
    MATERIAL_TEST_CASES = [
        {
            "test_id": "TC-201",
            "name": "Material missing name",
            "payload": {
                "materials": [{
                    "price": 100,
                    "quantity": 2,
                    "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
                }]
            },
            "expected_status": 422,
            "expected_error": "materials",
            "description": "Should reject material without name"
        },
        {
            "test_id": "TC-202",
            "name": "Material missing price",
            "payload": {
                "materials": [{
                    "name": "test material",
                    "quantity": 2,
                    "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
                }]
            },
            "expected_status": 422,
            "expected_error": "materials",
            "description": "Should reject material without price"
        },
        {
            "test_id": "TC-203",
            "name": "Material missing quantity",
            "payload": {
                "materials": [{
                    "name": "test material",
                    "price": 100,
                    "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
                }]
            },
            "expected_status": 422,
            "expected_error": "materials",
            "description": "Should reject material without quantity"
        },
        {
            "test_id": "TC-204",
            "name": "Material missing unit_id",
            "payload": {
                "materials": [{
                    "name": "test material",
                    "price": 100,
                    "quantity": 2
                }]
            },
            "expected_status": 422,
            "expected_error": "materials",
            "description": "Should reject material without unit_id"
        }
    ]