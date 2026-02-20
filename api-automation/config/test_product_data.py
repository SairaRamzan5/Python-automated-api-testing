"""Test data for Product Creation API tests - Updated with correct structure from successful test"""

import time
from datetime import datetime

class ProductTestData:
    """Test data configuration for product creation tests"""
    
    # API Validation limits from your response
    VALIDATION_LIMITS = {
        "name_max_length": 30,
        "materials_max": 100,
        "techniques_max": 50,
        "files_max": 15,
        "hours_min": 0.1,
        "monthly_qty_min": 1,
        "annual_qty_min": 12,
        "price_min": 0,
        "price_max": 999999.99
    }
    
    # CORRECTED: Valid test data with CORRECT STRUCTURE (array of objects)
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
        "techniques": [  # CORRECTED: Array of objects (not array of strings)
            {"id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849"}
        ],
        "files": [  # CORRECTED: Array of objects (not array of strings)
            {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"}
        ]
    }
    
    # Alternative file objects from your response
    ALTERNATIVE_FILES = [
        {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"},
        {"id": "78bbd7e5-c036-4544-aea6-0013838946cb"},
        {"id": "1faa4719-74f3-4e08-9ba4-741d40e70aba"},
        {"id": "9f990a97-ccc9-43b8-b877-9668557f06f3"},
        {"id": "b13e6538-45cb-4424-b7ff-a8c76001a39d"}
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
    def generate_unique_product_name(base_name="Product"):
        """Generate a unique product name within 30 character limit"""
        timestamp = int(time.time())
        # Keep within 30 characters
        name = f"{base_name} {timestamp}"
        if len(name) > 30:
            # Trim if needed
            max_base_length = 30 - len(f" {timestamp}")
            if max_base_length > 0:
                name = f"{base_name[:max_base_length]} {timestamp}"
            else:
                name = f"P{timestamp}"
        return name
    
    @staticmethod
    def get_valid_product_payload(**kwargs):
        """Get a valid product payload with optional overrides"""
        payload = ProductTestData.VALID_PRODUCT.copy()
        
        # Make name unique by default (within 30 char limit)
        if "name" not in kwargs:
            payload["name"] = ProductTestData.generate_unique_product_name()
        
        # Update with any provided kwargs
        payload.update(kwargs)
        return payload
    
    # ==================== POSITIVE TEST CASES ====================
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
            "name": "Create product with maximum files (15)",
            "payload": {
                "files": [
                    {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"},
                    {"id": "78bbd7e5-c036-4544-aea6-0013838946cb"},
                    {"id": "1faa4719-74f3-4e08-9ba4-741d40e70aba"},
                    {"id": "9f990a97-ccc9-43b8-b877-9668557f06f3"},
                    {"id": "b13e6538-45cb-4424-b7ff-a8c76001a39d"},
                    {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"},
                    {"id": "78bbd7e5-c036-4544-aea6-0013838946cb"},
                    {"id": "1faa4719-74f3-4e08-9ba4-741d40e70aba"},
                    {"id": "9f990a97-ccc9-43b8-b877-9668557f06f3"},
                    {"id": "b13e6538-45cb-4424-b7ff-a8c76001a39d"},
                    {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"},
                    {"id": "78bbd7e5-c036-4544-aea6-0013838946cb"},
                    {"id": "1faa4719-74f3-4e08-9ba4-741d40e70aba"},
                    {"id": "9f990a97-ccc9-43b8-b877-9668557f06f3"},
                    {"id": "b13e6538-45cb-4424-b7ff-a8c76001a39d"}
                ]
            },
            "expected_status": 201,
            "expected_fields": ["id", "files"],
            "description": "Should accept product with maximum 15 files"
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
            "name": "Create product with maximum techniques (50)",
            "payload": {
                "techniques": [{"id": f"tech-{i}"} for i in range(50)]
            },
            "expected_status": 201,
            "expected_fields": ["id", "techniques"],
            "description": "Should accept product with maximum 50 techniques"
        }
    ]
    
    # ==================== NEGATIVE TEST CASES ====================
    NEGATIVE_TEST_CASES = [
        {
            "test_id": "TC-101",
            "name": "Product name exceeds 30 characters",
            "payload": {
                "name": "This is a very long product name that exceeds the maximum allowed length of 30 characters"
            },
            "expected_status": 422,
            "expected_error": "name",
            "expected_message": "Product name must not exceed 30 characters",
            "description": "Should reject product name longer than 30 characters"
        },
        {
            "test_id": "TC-102",
            "name": "Empty name field",
            "payload": {"name": ""},
            "expected_status": 422,
            "expected_error": "name",
            "expected_message": "Product name is required",
            "description": "Should reject product with empty name"
        },
        {
            "test_id": "TC-103",
            "name": "Missing name field",
            "payload": {},  # Name will be set to None in test
            "remove_field": "name",  # Special flag to remove the field
            "expected_status": 422,
            "expected_error": "name",
            "expected_message": "Product name is required",
            "description": "Should reject product without name"
        },
        {
            "test_id": "TC-104",
            "name": "Invalid name type (number)",
            "payload": {"name": 12345},
            "expected_status": 422,
            "expected_error": "name",
            "expected_message": "Product name must be a string",
            "description": "Should reject non-string product name"
        },
        {
            "test_id": "TC-105",
            "name": "Too many materials (101)",
            "payload": {
                "materials": [
                    {
                        "name": f"Material {i}",
                        "price": 10,
                        "quantity": 1,
                        "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
                    }
                    for i in range(101)
                ]
            },
            "expected_status": 422,
            "expected_error": "materials",
            "expected_message": "Maximum 100 materials are allowed",
            "description": "Should reject more than 100 materials"
        },
        {
            "test_id": "TC-106",
            "name": "Invalid materials type (not array)",
            "payload": {"materials": "not-an-array"},
            "expected_status": 422,
            "expected_error": "materials",
            "expected_message": "Materials must be an array",
            "description": "Should reject non-array materials"
        },
        {
            "test_id": "TC-107",
            "name": "Too many techniques (51)",
            "payload": {
                "techniques": [{"id": f"tech-{i}"} for i in range(51)]
            },
            "expected_status": 422,
            "expected_error": "techniques",
            "expected_message": "Maximum 50 techniques are allowed",
            "description": "Should reject more than 50 techniques"
        },
        {
            "test_id": "TC-108",
            "name": "Invalid techniques type (not array)",
            "payload": {"techniques": "not-an-array"},
            "expected_status": 422,
            "expected_error": "techniques",
            "expected_message": "techniques must be an array",
            "description": "Should reject non-array techniques"
        },
        {
            "test_id": "TC-109",
            "name": "Too many files (16)",
            "payload": {
                "files": [{"id": f"file-{i}"} for i in range(16)]
            },
            "expected_status": 422,
            "expected_error": "files",
            "expected_message": "Maximum 15 files are allowed",
            "description": "Should reject more than 15 files"
        },
        {
            "test_id": "TC-110",
            "name": "Invalid files type (not array)",
            "payload": {"files": "not-an-array"},
            "expected_status": 422,
            "expected_error": "files",
            "expected_message": "files must be an array",
            "description": "Should reject non-array files"
        },
        {
            "test_id": "TC-111",
            "name": "Negative hours to make",
            "payload": {"hours_to_make": -1},
            "expected_status": 422,
            "expected_error": "hours_to_make",
            "description": "Should reject negative hours"
        },
        {
            "test_id": "TC-112",
            "name": "Zero hours to make",
            "payload": {"hours_to_make": 0},
            "expected_status": 422,
            "expected_error": "hours_to_make",
            "description": "Should reject zero hours"
        },
        {
            "test_id": "TC-113",
            "name": "Negative monthly quantity",
            "payload": {"monthly_qty": -10},
            "expected_status": 422,
            "expected_error": "monthly_qty",
            "description": "Should reject negative monthly quantity"
        },
        {
            "test_id": "TC-114",
            "name": "Negative annual quantity",
            "payload": {"annual_qty": -100},
            "expected_status": 422,
            "expected_error": "annual_qty",
            "description": "Should reject negative annual quantity"
        },
        {
            "test_id": "TC-115",
            "name": "Annual less than monthly quantity",
            "payload": {"annual_qty": 100, "monthly_qty": 200},
            "expected_status": 422,
            "expected_error": "annual_qty",
            "description": "Should reject annual less than monthly"
        },
        {
            "test_id": "TC-116",
            "name": "Negative custom price",
            "payload": {"custom_price": -5},
            "expected_status": 422,
            "expected_error": "custom_price",
            "description": "Should reject negative price"
        },
        {
            "test_id": "TC-117",
            "name": "Empty materials array",
            "payload": {"materials": []},
            "expected_status": 422,
            "expected_error": "materials",
            "description": "Should reject empty materials"
        },
        {
            "test_id": "TC-118",
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
        }
    ]
    
    # Test tags for filtering
    TEST_TAGS = {
        "smoke": ["TC-001", "TC-101", "TC-102"],
        "validation": ["TC-101", "TC-102", "TC-105", "TC-107", "TC-109"],
        "boundary": ["TC-003", "TC-005", "TC-105", "TC-107", "TC-109"],
        "regression": ["TC-001", "TC-002", "TC-004", "TC-101", "TC-111", "TC-116"],
        "security": []  # Add authentication test IDs here
    }