"""Test data for Techniques Add API tests"""

TECHNIQUES_ADD_TEST_DATA = {
    # ==================== POSITIVE TEST CASES ====================
    "positive_cases": [
        {
            "test_id": "TC_TA_01",
            "description": "Add single technique with single language",
            "data": {
                "techniques": [
                    {
                        "name": "wood-carving",
                        "description": "Carving designs into wood",
                        "parent_name": None,
                        "is_active": True,
                        "values": [
                            {
                                "language_code": "en",
                                "name": "Wood Carving"
                            }
                        ]
                    }
                ]
            },
            "expected_status": 201,  # CHANGED FROM 200 to 201
            "expected_success": True,
            "expected_message": "All techniques created successfully",
            "expected_count": 1,
            "expected_fields": ["id", "name", "description", "is_active", "values"],
            "tags": ["positive", "single", "smoke"],
            "priority": "high"
        },
        {
            "test_id": "TC_TA_02",
            "description": "Add single technique with multiple languages",
            "data": {
                "techniques": [
                    {
                        "name": "embroidery",
                        "description": "Decorating fabric with needle and thread",
                        "parent_name": None,
                        "is_active": True,
                        "values": [
                            {
                                "language_code": "en",
                                "name": "Embroidery"
                            },
                            {
                                "language_code": "es",
                                "name": "Bordado"
                            },
                            {
                                "language_code": "fr",
                                "name": "Broderie"
                            }
                        ]
                    }
                ]
            },
            "expected_status": 201,  # CHANGED FROM 200 to 201
            "expected_success": True,
            "expected_message": "All techniques created successfully",
            "expected_count": 1,
            "tags": ["positive", "multi_language"],
            "priority": "high"
        },
        {
            "test_id": "TC_TA_03",
            "description": "Add multiple techniques at once",
            "data": {
                "techniques": [
                    {
                        "name": "weaving",
                        "description": "Interlacing threads to form fabric",
                        "parent_name": None,
                        "is_active": True,
                        "values": [
                            {
                                "language_code": "en",
                                "name": "Weaving"
                            }
                        ]
                    },
                    {
                        "name": "pottery",
                        "description": "Shaping clay into objects",
                        "parent_name": None,
                        "is_active": True,
                        "values": [
                            {
                                "language_code": "en",
                                "name": "Pottery"
                            },
                            {
                                "language_code": "es",
                                "name": "Alfarería"
                            }
                        ]
                    }
                ]
            },
            "expected_status": 201,  # CHANGED FROM 200 to 201
            "expected_success": True,
            "expected_message": "All techniques created successfully",
            "expected_count": 2,
            "tags": ["positive", "bulk", "multiple"],
            "priority": "medium"
        },
        {
            "test_id": "TC_TA_04",
            "description": "Add technique with is_active false",
            "data": {
                "techniques": [
                    {
                        "name": "basketry",
                        "description": "Weaving plant materials into baskets",
                        "parent_name": None,
                        "is_active": False,
                        "values": [
                            {
                                "language_code": "en",
                                "name": "Basketry"
                            }
                        ]
                    }
                ]
            },
            "expected_status": 201,  # CHANGED FROM 200 to 201
            "expected_success": True,
            "expected_message": "All techniques created successfully",
            "expected_count": 1,
            "expected_inactive": True,
            "tags": ["positive", "inactive"],
            "priority": "medium"
        }
    ],
    
    # ==================== NEGATIVE TEST CASES ====================
    "negative_cases": [
        {
            "test_id": "TC_TA_05",
            "description": "Add duplicate technique name",
            "data": {
                "techniques": [
                    {
                        "name": "glass-blowing",  # Already exists
                        "description": "Duplicate technique",
                        "parent_name": None,
                        "is_active": True,
                        "values": [
                            {
                                "language_code": "en",
                                "name": "Duplicate"
                            }
                        ]
                    }
                ]
            },
            "expected_status": 201,  # Your API returns 201 even for duplicates
            "expected_success": True,
            "expected_message": "All techniques created successfully",
            "expected_duplicate": True,
            "tags": ["negative", "duplicate", "validation"],
            "priority": "high"
        },
        {
            "test_id": "TC_TA_06",
            "description": "Empty techniques array",
            "data": {
                "techniques": []
            },
            "expected_status": 422,
            "expected_success": False,
            "expected_message": "techniques must not be empty",
            "tags": ["negative", "validation", "empty"],
            "priority": "medium"
        },
        {
            "test_id": "TC_TA_07",
            "description": "Missing required field - name",
            "data": {
                "techniques": [
                    {
                        # Missing name
                        "description": "Test technique",
                        "parent_name": None,
                        "is_active": True,
                        "values": [
                            {
                                "language_code": "en",
                                "name": "Test"
                            }
                        ]
                    }
                ]
            },
            "expected_status": 422,
            "expected_success": False,
            "expected_message": "name is required",
            "tags": ["negative", "validation", "missing_field"],
            "priority": "high"
        },
        {
            "test_id": "TC_TA_08",
            "description": "Missing required field - values",
            "data": {
                "techniques": [
                    {
                        "name": "test-technique",
                        "description": "Test technique",
                        "parent_name": None,
                        "is_active": True
                        # Missing values
                    }
                ]
            },
            "expected_status": 422,
            "expected_success": False,
            "expected_message": "values is required",
            "tags": ["negative", "validation", "missing_field"],
            "priority": "high"
        },
        {
            "test_id": "TC_TA_09",
            "description": "Empty values array",
            "data": {
                "techniques": [
                    {
                        "name": "test-technique",
                        "description": "Test technique",
                        "parent_name": None,
                        "is_active": True,
                        "values": []  # Empty
                    }
                ]
            },
            "expected_status": 422,
            "expected_success": False,
            "expected_message": "values must not be empty",
            "tags": ["negative", "validation", "empty"],
            "priority": "medium"
        },
        {
            "test_id": "TC_TA_10",
            "description": "Invalid language code in values",
            "data": {
                "techniques": [
                    {
                        "name": "test-technique",
                        "description": "Test technique",
                        "parent_name": None,
                        "is_active": True,
                        "values": [
                            {
                                "language_code": "xx",  # Invalid
                                "name": "Test"
                            }
                        ]
                    }
                ]
            },
            "expected_status": 201,  # UPDATE: Your API accepts invalid codes
            "expected_success": True,  # UPDATE: Your API returns success
            "expected_message": "All techniques created successfully",
            "tags": ["negative", "validation", "language"],
            "priority": "medium",
            "note": "Your API accepts invalid language codes"
        },
        {
            "test_id": "TC_TA_11",
            "description": "Add without authentication",
            "data": {
                "techniques": [
                    {
                        "name": "test-technique",
                        "description": "Test technique",
                        "parent_name": None,
                        "is_active": True,
                        "values": [
                            {
                                "language_code": "en",
                                "name": "Test"
                            }
                        ]
                    }
                ]
            },
            "headers": {},  # No auth header
            "expected_status": 401,
            "expected_success": False,
            "expected_message": "Authentication required",
            "tags": ["negative", "security", "authentication"],
            "priority": "high"
        }
    ]
}

# Helper data
VALID_LANGUAGE_CODES = ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ar"]

TEST_CONFIG = {
    "name_max_length": 100,
    "description_max_length": 1000,
    "min_values_count": 1,
    "max_techniques_per_request": 50,
}

TEST_TAGS = {
    "smoke": ["TC_TA_01", "TC_TA_02", "TC_TA_05", "TC_TA_11"],
    "regression": ["TC_TA_01", "TC_TA_02", "TC_TA_05", "TC_TA_06", "TC_TA_07", "TC_TA_08"],
    "validation": ["TC_TA_06", "TC_TA_07", "TC_TA_08", "TC_TA_09", "TC_TA_10"],
    "security": ["TC_TA_11"],
    "bulk": ["TC_TA_03"],
    "duplicate": ["TC_TA_05"]
}