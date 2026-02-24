"""Test data for Product Creation API tests - Based on working payload structure"""

import time
import uuid

class ProductTestData:
    """Test data configuration for product creation tests"""
    
    # API Validation limits from successful response
    VALIDATION_LIMITS = {
        "name_max_length": 30,
        "materials_max": 100,
        "techniques_max": 50,
        "files_max": 15,
        "measurements_max": 20,
        "hours_min": 0.1,
        "monthly_qty_min": 1,
        "annual_qty_min": 12,
        "price_min": 0,
        "price_max": 999999.99
    }
    
    # Valid technique IDs from the system
    VALID_TECHNIQUE_IDS = [
        "fcae2e4e-b8b5-4a5f-b879-111896c2e849",
        "8fc243e7-d556-43b6-81a8-392d30b586c5"
    ]
    
    # Valid file IDs from the system
    VALID_FILE_IDS = [
        "58a82002-020b-4e12-917f-5fcb3dccd29d",
        "78bbd7e5-c036-4544-aea6-0013838946cb",
        "1faa4719-74f3-4e08-9ba4-741d40e70aba",
        "9f990a97-ccc9-43b8-b877-9668557f06f3",
        "b13e6538-45cb-4424-b7ff-a8c76001a39d"
    ]
    
    # Valid product payload based on working example
    VALID_PRODUCT = {
        "name": "Handcrafted Ceramic Mug",
        "description": "Beautiful handcrafted ceramic mug with unique design",
        "hours_to_make": 2.5,
        "monthly_qty": 50,
        "annual_qty": 600,
        "custom_price": 25.99,
        "is_active": True,
        "status": "pending",
        "workshops": [],
        "materials": [
            {
                "name": "Clay",
                "price": 15.0,
                "quantity": 2,
                "unit": "kg"
            },
            {
                "name": "Glaze",
                "price": 8.0,
                "quantity": 1,
                "unit": "liter"
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
        ],
        "measurements": [
            {
                "size": "Standard",
                "width": 8,
                "length": 8,
                "height": 10,
                "description": "Standard mug size"
            }
        ]
    }
    
    # Different status values from the system
    STATUS_VALUES = ["pending", "draft", "active", "inactive", "rejected"]
    
    @staticmethod
    def generate_unique_product_name(base_name="Test Product"):
        """Generate a unique product name within 30 character limit"""
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:4]
        name = f"{base_name} {timestamp}-{unique_id}"
        # Ensure within 30 characters
        if len(name) > 30:
            name = f"{base_name[:15]} {timestamp}"
        return name[:30]
    
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
    
    # ==================== POSITIVE TEST CASES ====================
    VALIDATION_TEST_CASES = [
        {
            "test_id": "TC-001",
            "name": "Create product with valid data",
            "payload": {},
            "expected_status": 201,
            "expected_fields": ["id", "name", "status", "materials", "techniques", "files"],
            "description": "Should create product successfully with all required fields"
        },
        {
            "test_id": "TC-002",
            "name": "Create product with multiple materials",
            "payload": {
                "materials": [
                    {"name": "Clay", "price": 15, "quantity": 2, "unit": "kg"},
                    {"name": "Glaze", "price": 8, "quantity": 1, "unit": "liter"},
                    {"name": "Paint", "price": 5, "quantity": 3, "unit": "piece"},
                    {"name": "Brushes", "price": 10, "quantity": 2, "unit": "piece"}
                ]
            },
            "expected_status": 201,
            "description": "Should accept product with multiple materials"
        },
        {
            "test_id": "TC-003",
            "name": "Create product with multiple techniques",
            "payload": {
                "techniques": [
                    {"id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849"},
                    {"id": "8fc243e7-d556-43b6-81a8-392d30b586c5"}
                ]
            },
            "expected_status": 201,
            "description": "Should accept product with multiple techniques"
        },
        {
            "test_id": "TC-004",
            "name": "Create product with multiple files",
            "payload": {
                "files": [
                    {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"},
                    {"id": "78bbd7e5-c036-4544-aea6-0013838946cb"},
                    {"id": "1faa4719-74f3-4e08-9ba4-741d40e70aba"}
                ]
            },
            "expected_status": 201,
            "description": "Should accept product with multiple files"
        },
        {
            "test_id": "TC-005",
            "name": "Create product with multiple measurements",
            "payload": {
                "measurements": [
                    {"size": "S", "width": 45, "length": 65, "height": 4, "description": "Small"},
                    {"size": "M", "width": 50, "length": 70, "height": 5, "description": "Medium"},
                    {"size": "L", "width": 55, "length": 75, "height": 6, "description": "Large"}
                ]
            },
            "expected_status": 201,
            "description": "Should accept product with multiple measurements"
        },
        {
            "test_id": "TC-006",
            "name": "Create product with active status",
            "payload": {
                "status": "active",
                "is_active": True
            },
            "expected_status": 201,
            "description": "Should accept product with active status"
        },
        {
            "test_id": "TC-007",
            "name": "Create product with zero custom price",
            "payload": {"custom_price": 0},
            "expected_status": 201,
            "description": "Should accept product with zero price"
        },
        {
            "test_id": "TC-008",
            "name": "Create product without measurements",
            "payload": {"measurements": []},
            "expected_status": 201,
            "description": "Should accept product without measurements"
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
            "description": "Should reject product name longer than 30 characters"
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
            "name": "Missing name field",
            "payload": {"remove_field": "name"},
            "expected_status": 422,
            "expected_error": "name",
            "description": "Should reject product without name"
        },
        {
            "test_id": "TC-104",
            "name": "Invalid name type (number)",
            "payload": {"name": 12345},
            "expected_status": 422,
            "expected_error": "name",
            "description": "Should reject non-string product name"
        },
        {
            "test_id": "TC-105",
            "name": "Too many materials (101)",
            "payload": {
                "materials": [
                    {"name": f"Material {i}", "price": 10, "quantity": 1, "unit": "piece"}
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
            "name": "Materials not an array",
            "payload": {"materials": {"name": "Clay", "price": 15, "quantity": 2, "unit": "kg"}},
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
            "name": "Techniques not an array",
            "payload": {"techniques": {"id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849"}},
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
            "name": "Files not an array",
            "payload": {"files": {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"}},
            "expected_status": 422,
            "expected_error": "files",
            "expected_message": "files must be an array",
            "description": "Should reject non-array files"
        },
        {
            "test_id": "TC-111",
            "name": "Too many measurements (21)",
            "payload": {
                "measurements": [
                    {"size": f"Size {i}", "width": 10, "length": 20, "height": 5}
                    for i in range(21)
                ]
            },
            "expected_status": 422,
            "expected_error": "measurements",
            "expected_message": "Maximum 20 measurements are allowed",
            "description": "Should reject more than 20 measurements"
        },
        {
            "test_id": "TC-112",
            "name": "Measurements not an array",
            "payload": {
                "measurements": {
                    "size": "M",
                    "width": 50,
                    "length": 70,
                    "height": 5,
                    "description": "Single measurement"
                }
            },
            "expected_status": 422,
            "expected_error": "measurements",
            "expected_message": "Measurements must be an array",
            "description": "Should reject non-array measurements"
        },
        {
            "test_id": "TC-113",
            "name": "Negative hours to make",
            "payload": {"hours_to_make": -1},
            "expected_status": 422,
            "expected_error": "hours_to_make",
            "description": "Should reject negative hours"
        },
        {
            "test_id": "TC-114",
            "name": "Zero hours to make",
            "payload": {"hours_to_make": 0},
            "expected_status": 422,
            "expected_error": "hours_to_make",
            "description": "Should reject zero hours"
        },
        {
            "test_id": "TC-115",
            "name": "Negative monthly quantity",
            "payload": {"monthly_qty": -10},
            "expected_status": 422,
            "expected_error": "monthly_qty",
            "description": "Should reject negative monthly quantity"
        },
        {
            "test_id": "TC-116",
            "name": "Negative annual quantity",
            "payload": {"annual_qty": -100},
            "expected_status": 422,
            "expected_error": "annual_qty",
            "description": "Should reject negative annual quantity"
        },
        {
            "test_id": "TC-117",
            "name": "Annual less than monthly quantity",
            "payload": {"annual_qty": 500, "monthly_qty": 100},
            "expected_status": 422,
            "expected_error": "annual_qty",
            "description": "Should reject annual less than monthly * 12"
        },
        {
            "test_id": "TC-118",
            "name": "Negative custom price",
            "payload": {"custom_price": -5},
            "expected_status": 422,
            "expected_error": "custom_price",
            "description": "Should reject negative price"
        }
    ]
    
    # Test tags for filtering
    TEST_TAGS = {
        "smoke": ["TC-001"],
        "positive": ["TC-001", "TC-002", "TC-003", "TC-004", "TC-005", "TC-006", "TC-007", "TC-008"],
        "negative": ["TC-101", "TC-102", "TC-103", "TC-104", "TC-105", "TC-106", "TC-107", "TC-108", 
                    "TC-109", "TC-110", "TC-111", "TC-112", "TC-113", "TC-114", "TC-115", "TC-116", 
                    "TC-117", "TC-118"],
        "boundary": ["TC-105", "TC-107", "TC-109", "TC-111"],
        "security": []
    }