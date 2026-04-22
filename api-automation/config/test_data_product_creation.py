# """Test data for Product Creation API tests - Based on working payload structure"""

# import time
# import uuid

# class ProductTestData:
#     """Test data configuration for product creation tests"""
    
#     # API Validation limits from successful response
#     VALIDATION_LIMITS = {
#         "name_max_length": 30,
#         "materials_max": 100,
#         "techniques_max": 50,
#         "files_max": 15,
#         "measurements_max": 20,
#         "hours_min": 0.1,
#         "monthly_qty_min": 1,
#         "annual_qty_min": 12,
#         "price_min": 0,
#         "price_max": 999999.99
#     }
    
#     # Valid technique IDs from the system
#     VALID_TECHNIQUE_IDS = [
#         "fcae2e4e-b8b5-4a5f-b879-111896c2e849",
#         "8fc243e7-d556-43b6-81a8-392d30b586c5"
#     ]
    
#     # Valid file IDs from the system
#     VALID_FILE_IDS = [
#         "58a82002-020b-4e12-917f-5fcb3dccd29d",
#         "78bbd7e5-c036-4544-aea6-0013838946cb",
#         "1faa4719-74f3-4e08-9ba4-741d40e70aba",
#         "9f990a97-ccc9-43b8-b877-9668557f06f3",
#         "b13e6538-45cb-4424-b7ff-a8c76001a39d"
#     ]
    
#     # Valid product payload based on working example
#     VALID_PRODUCT = {
#         "name": "Handcrafted Ceramic Mug",
#         "description": "Beautiful handcrafted ceramic mug with unique design",
#         "hours_to_make": 2.5,
#         "monthly_qty": 50,
#         "annual_qty": 600,
#         "custom_price": 25.99,
#         "is_active": True,
#         "status": "pending",
#         "workshops": [],
#         "materials": [
#             {
#                 "name": "Clay",
#                 "price": 15.0,
#                 "quantity": 2,
#                 "unit": "kg"
#             },
#             {
#                 "name": "Glaze",
#                 "price": 8.0,
#                 "quantity": 1,
#                 "unit": "liter"
#             }
#         ],
#         "techniques": [
#             {
#                 "id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849"
#             }
#         ],
#         "files": [
#             {
#                 "id": "58a82002-020b-4e12-917f-5fcb3dccd29d"
#             }
#         ],
#         "measurements": [
#             {
#                 "size": "Standard",
#                 "width": 8,
#                 "length": 8,
#                 "height": 10,
#                 "description": "Standard mug size"
#             }
#         ]
#     }
    
#     # Different status values from the system
#     STATUS_VALUES = ["pending", "draft", "active", "inactive", "rejected"]
    
#     @staticmethod
#     def generate_unique_product_name(base_name="Test Product"):
#         """Generate a unique product name within 30 character limit"""
#         timestamp = int(time.time())
#         unique_id = str(uuid.uuid4())[:4]
#         name = f"{base_name} {timestamp}-{unique_id}"
#         # Ensure within 30 characters
#         if len(name) > 30:
#             name = f"{base_name[:15]} {timestamp}"
#         return name[:30]
    
#     @staticmethod
#     def get_valid_product_payload(**kwargs):
#         """Get a valid product payload with optional overrides"""
#         payload = ProductTestData.VALID_PRODUCT.copy()
        
#         # Make name unique by default
#         if "name" not in kwargs:
#             payload["name"] = ProductTestData.generate_unique_product_name()
        
#         # Update with any provided kwargs
#         payload.update(kwargs)
#         return payload
    
#     # ==================== POSITIVE TEST CASES ====================
#     VALIDATION_TEST_CASES = [
#         {
#             "test_id": "TC-001",
#             "name": "Create product with valid data",
#             "payload": {},
#             "expected_status": 201,
#             "expected_fields": ["id", "name", "status", "materials", "techniques", "files"],
#             "description": "Should create product successfully with all required fields"
#         },
#         {
#             "test_id": "TC-002",
#             "name": "Create product with multiple materials",
#             "payload": {
#                 "materials": [
#                     {"name": "Clay", "price": 15, "quantity": 2, "unit": "kg"},
#                     {"name": "Glaze", "price": 8, "quantity": 1, "unit": "liter"},
#                     {"name": "Paint", "price": 5, "quantity": 3, "unit": "piece"},
#                     {"name": "Brushes", "price": 10, "quantity": 2, "unit": "piece"}
#                 ]
#             },
#             "expected_status": 201,
#             "description": "Should accept product with multiple materials"
#         },
#         {
#             "test_id": "TC-003",
#             "name": "Create product with multiple techniques",
#             "payload": {
#                 "techniques": [
#                     {"id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849"},
#                     {"id": "8fc243e7-d556-43b6-81a8-392d30b586c5"}
#                 ]
#             },
#             "expected_status": 201,
#             "description": "Should accept product with multiple techniques"
#         },
#         {
#             "test_id": "TC-004",
#             "name": "Create product with multiple files",
#             "payload": {
#                 "files": [
#                     {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"},
#                     {"id": "78bbd7e5-c036-4544-aea6-0013838946cb"},
#                     {"id": "1faa4719-74f3-4e08-9ba4-741d40e70aba"}
#                 ]
#             },
#             "expected_status": 201,
#             "description": "Should accept product with multiple files"
#         },
#         {
#             "test_id": "TC-005",
#             "name": "Create product with multiple measurements",
#             "payload": {
#                 "measurements": [
#                     {"size": "S", "width": 45, "length": 65, "height": 4, "description": "Small"},
#                     {"size": "M", "width": 50, "length": 70, "height": 5, "description": "Medium"},
#                     {"size": "L", "width": 55, "length": 75, "height": 6, "description": "Large"}
#                 ]
#             },
#             "expected_status": 201,
#             "description": "Should accept product with multiple measurements"
#         },
#         {
#             "test_id": "TC-006",
#             "name": "Create product with active status",
#             "payload": {
#                 "status": "active",
#                 "is_active": True
#             },
#             "expected_status": 201,
#             "description": "Should accept product with active status"
#         },
#         {
#             "test_id": "TC-007",
#             "name": "Create product with zero custom price",
#             "payload": {"custom_price": 0},
#             "expected_status": 201,
#             "description": "Should accept product with zero price"
#         },
#         {
#             "test_id": "TC-008",
#             "name": "Create product without measurements",
#             "payload": {"measurements": []},
#             "expected_status": 201,
#             "description": "Should accept product without measurements"
#         }
#     ]
    
#     # ==================== NEGATIVE TEST CASES ====================
#     NEGATIVE_TEST_CASES = [
#         {
#             "test_id": "TC-101",
#             "name": "Product name exceeds 30 characters",
#             "payload": {
#                 "name": "This is a very long product name that exceeds the maximum allowed length of 30 characters"
#             },
#             "expected_status": 422,
#             "expected_error": "name",
#             "description": "Should reject product name longer than 30 characters"
#         },
#         {
#             "test_id": "TC-102",
#             "name": "Empty name field",
#             "payload": {"name": ""},
#             "expected_status": 422,
#             "expected_error": "name",
#             "description": "Should reject product with empty name"
#         },
#         {
#             "test_id": "TC-103",
#             "name": "Missing name field",
#             "payload": {"remove_field": "name"},
#             "expected_status": 422,
#             "expected_error": "name",
#             "description": "Should reject product without name"
#         },
#         {
#             "test_id": "TC-104",
#             "name": "Invalid name type (number)",
#             "payload": {"name": 12345},
#             "expected_status": 422,
#             "expected_error": "name",
#             "description": "Should reject non-string product name"
#         },
#         {
#             "test_id": "TC-105",
#             "name": "Too many materials (101)",
#             "payload": {
#                 "materials": [
#                     {"name": f"Material {i}", "price": 10, "quantity": 1, "unit": "piece"}
#                     for i in range(101)
#                 ]
#             },
#             "expected_status": 422,
#             "expected_error": "materials",
#             "expected_message": "Maximum 100 materials are allowed",
#             "description": "Should reject more than 100 materials"
#         },
#         {
#             "test_id": "TC-106",
#             "name": "Materials not an array",
#             "payload": {"materials": {"name": "Clay", "price": 15, "quantity": 2, "unit": "kg"}},
#             "expected_status": 422,
#             "expected_error": "materials",
#             "expected_message": "Materials must be an array",
#             "description": "Should reject non-array materials"
#         },
#         {
#             "test_id": "TC-107",
#             "name": "Too many techniques (51)",
#             "payload": {
#                 "techniques": [{"id": f"tech-{i}"} for i in range(51)]
#             },
#             "expected_status": 422,
#             "expected_error": "techniques",
#             "expected_message": "Maximum 50 techniques are allowed",
#             "description": "Should reject more than 50 techniques"
#         },
#         {
#             "test_id": "TC-108",
#             "name": "Techniques not an array",
#             "payload": {"techniques": {"id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849"}},
#             "expected_status": 422,
#             "expected_error": "techniques",
#             "expected_message": "techniques must be an array",
#             "description": "Should reject non-array techniques"
#         },
#         {
#             "test_id": "TC-109",
#             "name": "Too many files (16)",
#             "payload": {
#                 "files": [{"id": f"file-{i}"} for i in range(16)]
#             },
#             "expected_status": 422,
#             "expected_error": "files",
#             "expected_message": "Maximum 15 files are allowed",
#             "description": "Should reject more than 15 files"
#         },
#         {
#             "test_id": "TC-110",
#             "name": "Files not an array",
#             "payload": {"files": {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d"}},
#             "expected_status": 422,
#             "expected_error": "files",
#             "expected_message": "files must be an array",
#             "description": "Should reject non-array files"
#         },
#         {
#             "test_id": "TC-111",
#             "name": "Too many measurements (21)",
#             "payload": {
#                 "measurements": [
#                     {"size": f"Size {i}", "width": 10, "length": 20, "height": 5}
#                     for i in range(21)
#                 ]
#             },
#             "expected_status": 422,
#             "expected_error": "measurements",
#             "expected_message": "Maximum 20 measurements are allowed",
#             "description": "Should reject more than 20 measurements"
#         },
#         {
#             "test_id": "TC-112",
#             "name": "Measurements not an array",
#             "payload": {
#                 "measurements": {
#                     "size": "M",
#                     "width": 50,
#                     "length": 70,
#                     "height": 5,
#                     "description": "Single measurement"
#                 }
#             },
#             "expected_status": 422,
#             "expected_error": "measurements",
#             "expected_message": "Measurements must be an array",
#             "description": "Should reject non-array measurements"
#         },
#         {
#             "test_id": "TC-113",
#             "name": "Negative hours to make",
#             "payload": {"hours_to_make": -1},
#             "expected_status": 422,
#             "expected_error": "hours_to_make",
#             "description": "Should reject negative hours"
#         },
#         {
#             "test_id": "TC-114",
#             "name": "Zero hours to make",
#             "payload": {"hours_to_make": 0},
#             "expected_status": 422,
#             "expected_error": "hours_to_make",
#             "description": "Should reject zero hours"
#         },
#         {
#             "test_id": "TC-115",
#             "name": "Negative monthly quantity",
#             "payload": {"monthly_qty": -10},
#             "expected_status": 422,
#             "expected_error": "monthly_qty",
#             "description": "Should reject negative monthly quantity"
#         },
#         {
#             "test_id": "TC-116",
#             "name": "Negative annual quantity",
#             "payload": {"annual_qty": -100},
#             "expected_status": 422,
#             "expected_error": "annual_qty",
#             "description": "Should reject negative annual quantity"
#         },
#         {
#             "test_id": "TC-117",
#             "name": "Annual less than monthly quantity",
#             "payload": {"annual_qty": 500, "monthly_qty": 100},
#             "expected_status": 422,
#             "expected_error": "annual_qty",
#             "description": "Should reject annual less than monthly * 12"
#         },
#         {
#             "test_id": "TC-118",
#             "name": "Negative custom price",
#             "payload": {"custom_price": -5},
#             "expected_status": 422,
#             "expected_error": "custom_price",
#             "description": "Should reject negative price"
#         }
#     ]
    
#     # Test tags for filtering
#     TEST_TAGS = {
#         "smoke": ["TC-001"],
#         "positive": ["TC-001", "TC-002", "TC-003", "TC-004", "TC-005", "TC-006", "TC-007", "TC-008"],
#         "negative": ["TC-101", "TC-102", "TC-103", "TC-104", "TC-105", "TC-106", "TC-107", "TC-108", 
#                     "TC-109", "TC-110", "TC-111", "TC-112", "TC-113", "TC-114", "TC-115", "TC-116", 
#                     "TC-117", "TC-118"],
#         "boundary": ["TC-105", "TC-107", "TC-109", "TC-111"],
#         "security": []
#     }


"""Test data for Product Creation API tests - Focused on data types and validation rules"""

import time
import uuid


class ProductTestData:
    """Test data configuration for product creation tests - Based on API validation rules"""
    
    # ==================== API VALIDATION LIMITS ====================
    VALIDATION_LIMITS = {
        "name_max_length": 30,
        "name_min_length": 1,
        "materials_max": 100,
        "techniques_max": 50,
        "files_max": 15,
        "measurements_max": 20,
        "hours_min": 0,
        "monthly_qty_min": 0,
        "annual_qty_min": 0,
        "price_min": 0,
        "price_max": 999999.99,
        "description_max_length": 500
    }
    
    # ==================== VALID STATUS VALUES ====================
    VALID_STATUSES = ["draft", "pending", "approved", "rejected", "available", "sent"]
    
    # ==================== INVALID STATUS VALUES ====================
    INVALID_STATUS_VALUES = [
        "active",           # Not in valid list
        "inactive",         # Not in valid list
        "published",        # Not in valid list
        "deleted",          # Not in valid list
        "archived",         # Not in valid list
        "PENDING",          # Uppercase
        "APPROVED",         # Uppercase
        "DRAFT",            # Uppercase
        "AVAILABLE",        # Uppercase
        "SENT",             # Uppercase
        " pending",         # Leading space
        "approved ",        # Trailing space
        "draft!",           # Special character
        "pending123",       # With numbers
        "",                 # Empty string
        " ",                # Space only
        123,                # Number
        True,               # Boolean
        None                # Null
    ]
    
    # ==================== VALID FIELD TYPE EXAMPLES ====================
    VALID_FIELD_TYPES = {
        "name": "Valid Product Name",
        "description": "This is a valid product description text",
        "hours_to_make": 2.5,
        "monthly_qty": 50,
        "annual_qty": 600,
        "custom_price": 25.99,
        "is_active": True,
        "status": "draft",
        "materials": [
            {"name": "Cotton", "price": 20.50, "quantity": 5, "unit": "kg"}
        ],
        "techniques": [
            {"id": "8fc243e7-d556-43b6-81a8-392d30b586c5", "deleted": False}
        ],
        "files": [
            {"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc", "is_active": True, "deleted": False}
        ],
        "measurements": [
            {"size": "Standard", "width": 10.5, "length": 10.5, "height": 15.0}
        ],
        "workshops": [
            {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "deleted": False}
        ]
    }
    
    # ==================== INVALID FIELD TYPES ====================
    INVALID_FIELD_TYPES = [
        # name field invalid types
        ("name", 12345, "must be string"),
        ("name", True, "must be string"),
        ("name", False, "must be string"),
        ("name", None, "must be string"),
        ("name", ["array"], "must be string"),
        ("name", {"object": "value"}, "must be string"),
        
        # description field invalid types
        ("description", 12345, "must be string"),
        ("description", True, "must be string"),
        ("description", ["array"], "must be string"),
        
        # hours_to_make invalid types
        ("hours_to_make", "invalid", "must be number"),
        ("hours_to_make", "50", "must be number"),
        ("hours_to_make", True, "must be number"),
        ("hours_to_make", None, "must be number"),
        ("hours_to_make", -5, "must be >= 0"),
        ("hours_to_make", -0.1, "must be >= 0"),
        
        # monthly_qty invalid types
        ("monthly_qty", "invalid", "must be number"),
        ("monthly_qty", "50", "must be number"),
        ("monthly_qty", True, "must be number"),
        ("monthly_qty", None, "must be number"),
        ("monthly_qty", -10, "must be >= 0"),
        
        # annual_qty invalid types
        ("annual_qty", "invalid", "must be number"),
        ("annual_qty", "600", "must be number"),
        ("annual_qty", True, "must be number"),
        ("annual_qty", None, "must be number"),
        ("annual_qty", -100, "must be >= 0"),
        
        # custom_price invalid types
        ("custom_price", "invalid", "must be number"),
        ("custom_price", "25.99", "must be number"),
        ("custom_price", True, "must be number"),
        ("custom_price", None, "must be number"),
        ("custom_price", -5.99, "must be >= 0"),
        
        # is_active invalid types
        ("is_active", "true", "must be boolean"),
        ("is_active", "false", "must be boolean"),
        ("is_active", 1, "must be boolean"),
        ("is_active", 0, "must be boolean"),
        ("is_active", "yes", "must be boolean"),
        ("is_active", "no", "must be boolean"),
        ("is_active", None, "must be boolean"),
        
        # status invalid types
        ("status", 123, "must be string"),
        ("status", True, "must be string"),
        ("status", ["draft"], "must be string"),
        
        # materials invalid types
        ("materials", "not_an_array", "must be array"),
        ("materials", {"key": "value"}, "must be array"),
        ("materials", "string", "must be array"),
        ("materials", 123, "must be array"),
        
        # techniques invalid types
        ("techniques", "not_an_array", "must be array"),
        ("techniques", {"key": "value"}, "must be array"),
        ("techniques", "string", "must be array"),
        ("techniques", 123, "must be array"),
        
        # files invalid types
        ("files", "not_an_array", "must be array"),
        ("files", {"key": "value"}, "must be array"),
        ("files", "string", "must be array"),
        ("files", 123, "must be array"),
        
        # measurements invalid types
        ("measurements", "not_an_array", "must be array"),
        ("measurements", {"key": "value"}, "must be array"),
        ("measurements", "string", "must be array"),
        ("measurements", 123, "must be array"),
        
        # workshops invalid types
        ("workshops", "not_an_array", "must be array"),
        ("workshops", {"key": "value"}, "must be array"),
        ("workshops", "string", "must be array"),
        ("workshops", 123, "must be array"),
    ]
    
    # ==================== EMPTY FIELD TESTS ====================
    EMPTY_FIELD_TESTS = [
        ("name", ""),
        ("name", "   "),  # Only spaces
        ("description", ""),
        ("description", "   "),
        ("status", ""),
        ("status", "   "),
        ("materials", []),
        ("techniques", []),
        ("files", []),
        ("measurements", []),
        ("workshops", []),
        ("hours_to_make", 0),
        ("monthly_qty", 0),
        ("annual_qty", 0),
        ("custom_price", 0),
    ]
    
    # ==================== BOUNDARY VALUE TESTS ====================
    BOUNDARY_TEST_CASES = [
        # Name boundaries
        {"name": "name_min_length_1", "field": "name", "value": "A", "should_pass": True},
        {"name": "name_max_length_30", "field": "name", "value": "X" * 30, "should_pass": True},
        {"name": "name_exceeds_max_31", "field": "name", "value": "X" * 31, "should_pass": False},
        {"name": "name_exceeds_max_100", "field": "name", "value": "X" * 100, "should_pass": False},
        
        # Hours boundaries
        {"name": "hours_min_0", "field": "hours_to_make", "value": 0, "should_pass": True},
        {"name": "hours_small_positive", "field": "hours_to_make", "value": 0.1, "should_pass": True},
        {"name": "hours_large", "field": "hours_to_make", "value": 9999.99, "should_pass": True},
        {"name": "hours_very_large", "field": "hours_to_make", "value": 999999.99, "should_pass": True},
        {"name": "hours_negative", "field": "hours_to_make", "value": -0.01, "should_pass": False},
        
        # Monthly quantity boundaries
        {"name": "monthly_qty_min_0", "field": "monthly_qty", "value": 0, "should_pass": True},
        {"name": "monthly_qty_small", "field": "monthly_qty", "value": 1, "should_pass": True},
        {"name": "monthly_qty_large", "field": "monthly_qty", "value": 99999, "should_pass": True},
        {"name": "monthly_qty_very_large", "field": "monthly_qty", "value": 9999999, "should_pass": True},
        {"name": "monthly_qty_negative", "field": "monthly_qty", "value": -1, "should_pass": False},
        
        # Annual quantity boundaries
        {"name": "annual_qty_min_0", "field": "annual_qty", "value": 0, "should_pass": True},
        {"name": "annual_qty_small", "field": "annual_qty", "value": 12, "should_pass": True},
        {"name": "annual_qty_large", "field": "annual_qty", "value": 999999, "should_pass": True},
        {"name": "annual_qty_negative", "field": "annual_qty", "value": -1, "should_pass": False},
        
        # Price boundaries
        {"name": "price_min_0", "field": "custom_price", "value": 0, "should_pass": True},
        {"name": "price_small", "field": "custom_price", "value": 0.01, "should_pass": True},
        {"name": "price_large", "field": "custom_price", "value": 999999.99, "should_pass": True},
        {"name": "price_negative", "field": "custom_price", "value": -0.01, "should_pass": False},
        
        # Description boundaries
        {"name": "description_empty", "field": "description", "value": "", "should_pass": True},
        {"name": "description_max_500", "field": "description", "value": "X" * 500, "should_pass": True},
        {"name": "description_exceeds_501", "field": "description", "value": "X" * 501, "should_pass": False},
    ]
    
    # ==================== MATERIALS VALIDATION TEST CASES ====================
    MATERIALS_TEST_CASES = [
        # Valid cases
        {
            "name": "single_material",
            "materials": [{"name": "Clay", "price": 15.0, "quantity": 2, "unit": "kg"}],
            "should_pass": True
        },
        {
            "name": "multiple_materials_2",
            "materials": [
                {"name": "Clay", "price": 15.0, "quantity": 2, "unit": "kg"},
                {"name": "Glaze", "price": 8.0, "quantity": 1, "unit": "liter"}
            ],
            "should_pass": True
        },
        {
            "name": "multiple_materials_5",
            "materials": [
                {"name": f"Material_{i}", "price": 10.0 * i, "quantity": i, "unit": "pc"}
                for i in range(1, 6)
            ],
            "should_pass": True
        },
        {
            "name": "max_materials_100",
            "materials": [{"name": f"Material_{i}", "price": 10.0, "quantity": 1, "unit": "pc"} for i in range(100)],
            "should_pass": True
        },
        {
            "name": "materials_with_string_price",
            "materials": [{"name": "Clay", "price": "15.0", "quantity": 2, "unit": "kg"}],
            "should_pass": True
        },
        {
            "name": "materials_with_string_quantity",
            "materials": [{"name": "Clay", "price": 15.0, "quantity": "2", "unit": "kg"}],
            "should_pass": True
        },
        
        # Invalid cases
        {
            "name": "exceeds_max_materials_101",
            "materials": [{"name": f"Material_{i}", "price": 10.0, "quantity": 1, "unit": "pc"} for i in range(101)],
            "should_pass": False
        },
        {
            "name": "empty_materials_array",
            "materials": [],
            "should_pass": True  # According to schema, empty array is acceptable
        },
        {
            "name": "material_missing_name",
            "materials": [{"price": 15.0, "quantity": 2, "unit": "kg"}],
            "should_pass": False
        },
        {
            "name": "material_missing_price",
            "materials": [{"name": "Clay", "quantity": 2, "unit": "kg"}],
            "should_pass": False
        },
        {
            "name": "material_missing_quantity",
            "materials": [{"name": "Clay", "price": 15.0, "unit": "kg"}],
            "should_pass": False
        },
        {
            "name": "material_missing_unit",
            "materials": [{"name": "Clay", "price": 15.0, "quantity": 2}],
            "should_pass": False
        },
        {
            "name": "material_negative_price",
            "materials": [{"name": "Clay", "price": -5.0, "quantity": 2, "unit": "kg"}],
            "should_pass": False
        },
        {
            "name": "material_negative_quantity",
            "materials": [{"name": "Clay", "price": 15.0, "quantity": -2, "unit": "kg"}],
            "should_pass": False
        },
        {
            "name": "material_zero_price",
            "materials": [{"name": "Clay", "price": 0, "quantity": 2, "unit": "kg"}],
            "should_pass": True  # Zero price might be acceptable
        },
        {
            "name": "material_zero_quantity",
            "materials": [{"name": "Clay", "price": 15.0, "quantity": 0, "unit": "kg"}],
            "should_pass": True  # Zero quantity might be acceptable
        },
        {
            "name": "material_extra_fields",
            "materials": [{"name": "Clay", "price": 15.0, "quantity": 2, "unit": "kg", "extra": "field"}],
            "should_pass": True  # Extra fields might be ignored
        },
    ]
    
    # ==================== TECHNIQUES VALIDATION TEST CASES ====================
    TECHNIQUES_TEST_CASES = [
        # Valid cases
        {
            "name": "single_technique",
            "techniques": [{"id": "8fc243e7-d556-43b6-81a8-392d30b586c5", "deleted": False}],
            "should_pass": True
        },
        {
            "name": "single_technique_without_deleted",
            "techniques": [{"id": "8fc243e7-d556-43b6-81a8-392d30b586c5"}],
            "should_pass": True
        },
        {
            "name": "multiple_techniques_2",
            "techniques": [
                {"id": "8fc243e7-d556-43b6-81a8-392d30b586c5", "deleted": False},
                {"id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849", "deleted": False}
            ],
            "should_pass": True
        },
        {
            "name": "multiple_techniques_5",
            "techniques": [
                {"id": f"test-id-{i}", "deleted": False} for i in range(5)
            ],
            "should_pass": True
        },
        {
            "name": "max_techniques_50",
            "techniques": [{"id": f"test-id-{i}", "deleted": False} for i in range(50)],
            "should_pass": True
        },
        {
            "name": "techniques_with_deleted_true",
            "techniques": [{"id": "8fc243e7-d556-43b6-81a8-392d30b586c5", "deleted": True}],
            "should_pass": True
        },
        
        # Invalid cases
        {
            "name": "exceeds_max_techniques_51",
            "techniques": [{"id": f"test-id-{i}", "deleted": False} for i in range(51)],
            "should_pass": False
        },
        {
            "name": "empty_techniques_array",
            "techniques": [],
            "should_pass": True
        },
        {
            "name": "technique_missing_id",
            "techniques": [{"deleted": False}],
            "should_pass": False
        },
        {
            "name": "technique_empty_string_id",
            "techniques": [{"id": "", "deleted": False}],
            "should_pass": False
        },
        {
            "name": "technique_null_id",
            "techniques": [{"id": None, "deleted": False}],
            "should_pass": False
        },
        {
            "name": "technique_invalid_uuid_format",
            "techniques": [{"id": "invalid-uuid-format", "deleted": False}],
            "should_pass": False
        },
        {
            "name": "technique_number_id",
            "techniques": [{"id": 12345, "deleted": False}],
            "should_pass": False
        },
        {
            "name": "technique_extra_fields",
            "techniques": [{"id": "8fc243e7-d556-43b6-81a8-392d30b586c5", "deleted": False, "extra": "field"}],
            "should_pass": True  # Extra fields might be ignored
        },
    ]
    
    # ==================== FILES VALIDATION TEST CASES ====================
    FILES_TEST_CASES = [
        # Valid cases
        {
            "name": "single_file",
            "files": [{"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc", "is_active": True, "deleted": False}],
            "should_pass": True
        },
        {
            "name": "single_file_without_is_active",
            "files": [{"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc", "deleted": False}],
            "should_pass": True
        },
        {
            "name": "single_file_without_deleted",
            "files": [{"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc", "is_active": True}],
            "should_pass": True
        },
        {
            "name": "single_file_minimum_fields",
            "files": [{"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc"}],
            "should_pass": True
        },
        {
            "name": "multiple_files_2",
            "files": [
                {"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc", "is_active": True, "deleted": False},
                {"id": "58a82002-020b-4e12-917f-5fcb3dccd29d", "is_active": True, "deleted": False}
            ],
            "should_pass": True
        },
        {
            "name": "multiple_files_5",
            "files": [
                {"id": f"test-file-{i}", "is_active": True, "deleted": False} for i in range(5)
            ],
            "should_pass": True
        },
        {
            "name": "max_files_15",
            "files": [{"id": f"test-file-{i}", "is_active": True, "deleted": False} for i in range(15)],
            "should_pass": True
        },
        {
            "name": "files_with_is_active_false",
            "files": [{"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc", "is_active": False, "deleted": False}],
            "should_pass": True
        },
        
        # Invalid cases
        {
            "name": "exceeds_max_files_16",
            "files": [{"id": f"test-file-{i}", "is_active": True, "deleted": False} for i in range(16)],
            "should_pass": False
        },
        {
            "name": "empty_files_array",
            "files": [],
            "should_pass": True
        },
        {
            "name": "file_missing_id",
            "files": [{"is_active": True, "deleted": False}],
            "should_pass": False
        },
        {
            "name": "file_empty_string_id",
            "files": [{"id": "", "is_active": True, "deleted": False}],
            "should_pass": False
        },
        {
            "name": "file_null_id",
            "files": [{"id": None, "is_active": True, "deleted": False}],
            "should_pass": False
        },
        {
            "name": "file_number_id",
            "files": [{"id": 12345, "is_active": True, "deleted": False}],
            "should_pass": False
        },
        {
            "name": "file_invalid_uuid_format",
            "files": [{"id": "invalid-uuid", "is_active": True, "deleted": False}],
            "should_pass": False
        },
        {
            "name": "file_extra_fields",
            "files": [{"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc", "is_active": True, "deleted": False, "extra": "field"}],
            "should_pass": True  # Extra fields might be ignored
        },
    ]
    
    # ==================== MEASUREMENTS VALIDATION TEST CASES ====================
    MEASUREMENTS_TEST_CASES = [
        # Valid cases
        {
            "name": "single_measurement_minimum",
            "measurements": [{"size": "M", "width": 10.5, "length": 10.5, "height": 15.0}],
            "should_pass": True
        },
        {
            "name": "single_measurement_with_description",
            "measurements": [{"size": "M", "width": 10.5, "length": 10.5, "height": 15.0, "description": "Standard size"}],
            "should_pass": True
        },
        {
            "name": "multiple_measurements_2",
            "measurements": [
                {"size": "S", "width": 8.0, "length": 8.0, "height": 10.0},
                {"size": "M", "width": 10.5, "length": 10.5, "height": 15.0}
            ],
            "should_pass": True
        },
        {
            "name": "multiple_measurements_5",
            "measurements": [
                {"size": f"Size_{i}", "width": 10.0, "length": 10.0, "height": 10.0} for i in range(5)
            ],
            "should_pass": True
        },
        {
            "name": "max_measurements_20",
            "measurements": [
                {"size": f"Size_{i}", "width": 10.0, "length": 10.0, "height": 10.0} for i in range(20)
            ],
            "should_pass": True
        },
        {
            "name": "measurement_with_string_dimensions",
            "measurements": [{"size": "M", "width": "10.5", "length": "10.5", "height": "15.0"}],
            "should_pass": True
        },
        {
            "name": "measurement_zero_dimensions",
            "measurements": [{"size": "M", "width": 0, "length": 0, "height": 0}],
            "should_pass": True
        },
        
        # Invalid cases
        {
            "name": "exceeds_max_measurements_21",
            "measurements": [
                {"size": f"Size_{i}", "width": 10.0, "length": 10.0, "height": 10.0} for i in range(21)
            ],
            "should_pass": False
        },
        {
            "name": "empty_measurements_array",
            "measurements": [],
            "should_pass": True
        },
        {
            "name": "measurement_missing_size",
            "measurements": [{"width": 10.5, "length": 10.5, "height": 15.0}],
            "should_pass": False
        },
        {
            "name": "measurement_missing_width",
            "measurements": [{"size": "M", "length": 10.5, "height": 15.0}],
            "should_pass": False
        },
        {
            "name": "measurement_missing_length",
            "measurements": [{"size": "M", "width": 10.5, "height": 15.0}],
            "should_pass": False
        },
        {
            "name": "measurement_missing_height",
            "measurements": [{"size": "M", "width": 10.5, "length": 10.5}],
            "should_pass": False
        },
        {
            "name": "measurement_negative_width",
            "measurements": [{"size": "M", "width": -10.5, "length": 10.5, "height": 15.0}],
            "should_pass": False
        },
        {
            "name": "measurement_negative_length",
            "measurements": [{"size": "M", "width": 10.5, "length": -10.5, "height": 15.0}],
            "should_pass": False
        },
        {
            "name": "measurement_negative_height",
            "measurements": [{"size": "M", "width": 10.5, "length": 10.5, "height": -15.0}],
            "should_pass": False
        },
    ]
    
    # ==================== WORKSHOPS VALIDATION TEST CASES ====================
    WORKSHOPS_TEST_CASES = [
        # Valid cases
        {
            "name": "single_workshop",
            "workshops": [{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "deleted": False}],
            "should_pass": True
        },
        {
            "name": "single_workshop_without_deleted",
            "workshops": [{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}],
            "should_pass": True
        },
        {
            "name": "multiple_workshops",
            "workshops": [
                {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "deleted": False},
                {"id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849", "deleted": False}
            ],
            "should_pass": True
        },
        {
            "name": "empty_workshops_array",
            "workshops": [],
            "should_pass": True
        },
        {
            "name": "workshop_with_deleted_true",
            "workshops": [{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "deleted": True}],
            "should_pass": True
        },
        
        # Invalid cases
        {
            "name": "workshop_missing_id",
            "workshops": [{"deleted": False}],
            "should_pass": False
        },
        {
            "name": "workshop_empty_string_id",
            "workshops": [{"id": "", "deleted": False}],
            "should_pass": False
        },
        {
            "name": "workshop_null_id",
            "workshops": [{"id": None, "deleted": False}],
            "should_pass": False
        },
        {
            "name": "workshop_invalid_uuid",
            "workshops": [{"id": "invalid-uuid", "deleted": False}],
            "should_pass": False
        },
    ]
    
    # ==================== QUANTITY RELATIONSHIP TESTS ====================
    QUANTITY_RELATIONSHIP_TESTS = [
        # Valid relationships
        (0, 0, True),           # Both zero
        (1, 12, True),          # Exactly monthly * 12
        (5, 60, True),          # Exactly monthly * 12
        (10, 120, True),        # Exactly monthly * 12
        (50, 600, True),        # Exactly monthly * 12
        (100, 1200, True),      # Exactly monthly * 12
        (50, 700, True),        # Greater than monthly * 12
        (100, 2000, True),      # Greater than monthly * 12
        (25, 500, True),        # Greater than monthly * 12 (300 < 500)
        (75, 1000, True),       # Greater than monthly * 12 (900 < 1000)
        
        # Invalid relationships
        (1, 11, False),         # Less than monthly * 12
        (5, 59, False),         # Less than monthly * 12
        (10, 100, False),       # Less than monthly * 12 (120 > 100)
        (50, 599, False),       # Less than monthly * 12
        (100, 1000, False),     # Less than monthly * 12 (1200 > 1000)
        (25, 200, False),       # Less than monthly * 12 (300 > 200)
        (75, 800, False),       # Less than monthly * 12 (900 > 800)
        (200, 2000, False),     # Less than monthly * 12 (2400 > 2000)
    ]
    
    # ==================== MISSING REQUIRED FIELDS TESTS ====================
    MISSING_FIELDS_TESTS = [
        {"name": "missing_name", "remove_field": "name", "should_fail": True},
        {"name": "missing_description", "remove_field": "description", "should_fail": False},
        {"name": "missing_hours_to_make", "remove_field": "hours_to_make", "should_fail": False},
        {"name": "missing_monthly_qty", "remove_field": "monthly_qty", "should_fail": False},
        {"name": "missing_annual_qty", "remove_field": "annual_qty", "should_fail": False},
        {"name": "missing_custom_price", "remove_field": "custom_price", "should_fail": False},
        {"name": "missing_is_active", "remove_field": "is_active", "should_fail": False},
        {"name": "missing_status", "remove_field": "status", "should_fail": False},
        {"name": "missing_materials", "remove_field": "materials", "should_fail": False},
        {"name": "missing_techniques", "remove_field": "techniques", "should_fail": False},
        {"name": "missing_files", "remove_field": "files", "should_fail": False},
        {"name": "missing_measurements", "remove_field": "measurements", "should_fail": False},
    ]
    
    # ==================== HELPER METHODS ====================
    
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
        payload = {
            "name": ProductTestData.generate_unique_product_name(),
            "description": "This is a test product created for API validation",
            "hours_to_make": 2.5,
            "monthly_qty": 50,
            "annual_qty": 600,
            "custom_price": 25.99,
            "is_active": True,
            "status": "draft",
            "workshops": [],
            "materials": [
                {
                    "name": "Cotton",
                    "price": 20.50,
                    "quantity": 5,
                    "unit": "kg"
                }
            ],
            "techniques": [
                {
                    "id": "8fc243e7-d556-43b6-81a8-392d30b586c5",
                    "deleted": False
                }
            ],
            "files": [
                {
                    "id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc",
                    "is_active": True,
                    "deleted": False
                }
            ],
            "measurements": [
                {
                    "size": "Standard",
                    "width": 10.5,
                    "length": 10.5,
                    "height": 15.0,
                    "description": "Standard size measurement"
                }
            ]
        }
        
        # Update with any provided kwargs
        payload.update(kwargs)
        
        # Handle field removal if specified
        if kwargs.get("remove_field"):
            field_to_remove = kwargs["remove_field"]
            if field_to_remove in payload:
                del payload[field_to_remove]
            if "remove_field" in payload:
                del payload["remove_field"]
        
        return payload
    
    @staticmethod
    def get_payload_without_field(field_name):
        """Get payload with a specific field removed"""
        payload = ProductTestData.get_valid_product_payload()
        if field_name in payload:
            del payload[field_name]
        return payload
    
    # ==================== TEST TAGS FOR FILTERING ====================
    TEST_TAGS = {
        "smoke": [
            "test_scenario_complete_valid_product",
            "test_scenario_minimum_required_fields"
        ],
        "positive": [
            "test_scenario_complete_valid_product",
            "test_scenario_minimum_required_fields",
            "test_scenario_different_status_values",
            "test_scenario_is_active_flag"
        ],
        "negative": [
            "test_scenario_invalid_status_values",
            "test_scenario_invalid_field_types",
            "test_scenario_annual_vs_monthly_quantity",
            "test_scenario_duplicate_product_name"
        ],
        "boundary": ["test_scenario_boundary_values"],
        "validation": [
            "test_scenario_materials_validation",
            "test_scenario_techniques_validation",
            "test_scenario_files_validation",
            "test_scenario_measurements_validation"
        ],
        "security": ["test_scenario_missing_authentication"],
        "empty_fields": ["test_scenario_empty_fields"]
    }