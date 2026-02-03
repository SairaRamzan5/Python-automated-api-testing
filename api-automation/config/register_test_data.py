"""
Test data for registration API tests - CORRECTED VERSION

Field Requirements:
- phone: REQUIRED
- password: REQUIRED
- f_name: OPTIONAL
- l_name: OPTIONAL
- email: OPTIONAL
"""

import uuid
import time
import random

# ============================================
# DATA GENERATORS
# ============================================

def generate_unique_email(base="artisan"):
    """Generate a unique email for testing"""
    timestamp = int(time.time() * 1000)
    return f"{base}_{timestamp}_{uuid.uuid4().hex[:4]}@test.com"

def generate_unique_phone():
    """Generate a unique phone number for testing (Bangladesh format)"""
    phone_suffix = ''.join(str(random.randint(0, 9)) for _ in range(8))
    return f"+88017{phone_suffix}"

def generate_unique_pk_phone():
    """Generate a unique Pakistan phone number"""
    suffix = ''.join(str(random.randint(0, 9)) for _ in range(9))
    return f"+92{suffix}"

# ============================================
# ARTISAN REGISTRATION TEST DATA
# ============================================

ARTISAN_REG_TEST_CASES = [

    # TC_Artisan_Reg_01: Valid Registration with All Fields
    {
        "test_id": "TC_Artisan_Reg_01",
        "description": "Valid artisan registration with all fields",
        "data_factory": lambda: {
            "f_name": "Artisan",
            "l_name": "Test",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("artisan"),
            "password": "SecurePass123!"
        },
        "expected_status": 201,
        "expected_success": True,
        "expected_message": "Register Successfully",
        "should_have_user_data": True,
        "expected_user_fields": ["id", "phone", "email", "phone_verified", "email_verified"],
        "tags": ["smoke", "positive", "critical"]
    },

    # TC_Artisan_Reg_02: Duplicate Email Registration
    {
        "test_id": "TC_Artisan_Reg_02",
        "description": "Registration with duplicate email",
        "data_factory": lambda: {
            "f_name": "Duplicate",
            "l_name": "User",
            "phone": generate_unique_phone(),
            "email": "existing@example.com",
            "password": "SecurePass123!"
        },
        "expected_status": 409,
        "expected_success": False,
        "expected_message": "User already exists",
        "skip": True,
        "tags": ["negative", "duplicate"]
    },

    # TC_Artisan_Reg_03: Duplicate Phone Registration
    {
        "test_id": "TC_Artisan_Reg_03",
        "description": "Registration with duplicate phone",
        "data_factory": lambda: {
            "f_name": "Duplicate",
            "l_name": "Phone",
            "phone": "+8801712345678",
            "email": generate_unique_email("duplicate_phone"),
            "password": "SecurePass123!"
        },
        "expected_status": 409,
        "expected_success": False,
        "expected_message": "User already exists",
        "skip": True,
        "tags": ["negative", "duplicate"]
    },

    # TC_Artisan_Reg_04: Invalid Email Format
    {
        "test_id": "TC_Artisan_Reg_04",
        "description": "Invalid email format",
        "data_factory": lambda: {
            "f_name": "Invalid",
            "l_name": "Email",
            "phone": generate_unique_phone(),
            "email": "not-an-email",
            "password": "SecurePass123!"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": ["email"],
        "tags": ["negative", "validation"]
    },

    # TC_Artisan_Reg_05: Weak Password
    {
        "test_id": "TC_Artisan_Reg_05",
        "description": "Weak password rejected",
        "data_factory": lambda: {
            "f_name": "Weak",
            "l_name": "Password",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("weakpass"),
            "password": "123"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": ["password"],
        "tags": ["negative", "validation"]
    },

    # TC_Artisan_Reg_06: Missing f_name
    {
        "test_id": "TC_Artisan_Reg_06",
        "description": "Missing optional first name",
        "data_factory": lambda: {
            "l_name": "Test",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("no_fname"),
            "password": "SecurePass123!"
        },
        "expected_status": 201,
        "expected_success": True,
        "expected_message": "Register Successfully",
        "should_have_user_data": True,
        "tags": ["positive", "optional_fields"]
    },

    # TC_Artisan_Reg_07: Missing l_name
    {
        "test_id": "TC_Artisan_Reg_07",
        "description": "Missing optional last name",
        "data_factory": lambda: {
            "f_name": "Test",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("no_lname"),
            "password": "SecurePass123!"
        },
        "expected_status": 201,
        "expected_success": True,
        "expected_message": "Register Successfully",
        "should_have_user_data": True,
        "tags": ["positive", "optional_fields"]
    },

    # TC_Artisan_Reg_08: Missing email
    {
        "test_id": "TC_Artisan_Reg_08",
        "description": "Missing optional email",
        "data_factory": lambda: {
            "f_name": "No",
            "l_name": "Email",
            "phone": generate_unique_phone(),
            "password": "SecurePass123!"
        },
        "expected_status": 201,
        "expected_success": True,
        "expected_message": "Register Successfully",
        "should_have_user_data": True,
        "tags": ["positive", "optional_fields"]
    },

    # TC_Artisan_Reg_09: Missing phone
    {
        "test_id": "TC_Artisan_Reg_09",
        "description": "Missing required phone",
        "data_factory": lambda: {
            "f_name": "No",
            "l_name": "Phone",
            "email": generate_unique_email("no_phone"),
            "password": "SecurePass123!"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": ["phone"],
        "tags": ["negative", "validation", "required_fields"]
    },

    # TC_Artisan_Reg_10: Missing password
    {
        "test_id": "TC_Artisan_Reg_10",
        "description": "Missing required password",
        "data_factory": lambda: {
            "f_name": "No",
            "l_name": "Password",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("no_pass")
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": ["password"],
        "tags": ["negative", "validation", "required_fields"]
    },

    # TC_Artisan_Reg_11: Invalid Phone Format
    {
        "test_id": "TC_Artisan_Reg_11",
        "description": "Invalid phone format",
        "data_factory": lambda: {
            "f_name": "Invalid",
            "l_name": "Phone",
            "phone": "abc123",
            "email": generate_unique_email("invalid_phone"),
            "password": "SecurePass123!"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": ["phone"],
        "tags": ["negative", "validation"]
    },

    # TC_Artisan_Reg_12: Minimal valid registration
    {
        "test_id": "TC_Artisan_Reg_12",
        "description": "Only required fields",
        "data_factory": lambda: {
            "phone": generate_unique_phone(),
            "password": "SecurePass123!"
        },
        "expected_status": 201,
        "expected_success": True,
        "expected_message": "Register Successfully",
        "should_have_user_data": True,
        "expected_user_fields": ["id", "phone", "phone_verified"],
        "tags": ["positive", "minimal", "critical"]
    },

    # TC_Artisan_Reg_13: SQL Injection
    {
        "test_id": "TC_Artisan_Reg_13",
        "description": "SQL injection attempt",
        "data_factory": lambda: {
            "f_name": "Robert'); DROP TABLE users;--",
            "l_name": "Test",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("sql"),
            "password": "SecurePass123!"
        },
        "expected_status": 422,
        "expected_success": False,
        "tags": ["security"]
    },

    # TC_Artisan_Reg_14: XSS
    {
        "test_id": "TC_Artisan_Reg_14",
        "description": "XSS attempt",
        "data_factory": lambda: {
            "f_name": "<script>alert(1)</script>",
            "l_name": "Test",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("xss"),
            "password": "SecurePass123!"
        },
        "expected_status": 422,
        "expected_success": False,
        "tags": ["security"]
    },

    # TC_Artisan_Reg_15: Phone with space
    {
        "test_id": "TC_Artisan_Reg_15",
        "description": "Phone with space after country code",
        "data_factory": lambda: {
            "f_name": "Amina",
            "l_name": "Iqbal",
            "phone": "+92 3048942431",
            "email": generate_unique_email("space_phone"),
            "password": "aminaIqbal@969000"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_errors": ["phone"],
        "tags": ["negative", "validation"]
    },

    # TC_Artisan_Reg_16: Valid Pakistan phone
    {
        "test_id": "TC_Artisan_Reg_16",
        "description": "Valid Pakistan phone format",
        "data_factory": lambda: {
            "f_name": "Amina",
            "l_name": "Iqbal",
            "phone": generate_unique_pk_phone(),
            "email": generate_unique_email("pk"),
            "password": "aminaIqbal@969000"
        },
        "expected_status": 201,
        "expected_success": True,
        "expected_message": "Register Successfully",
        "should_have_user_data": True,
        "tags": ["positive"]
    },

    # TC_006: Weak password rejected
    {
        "test_id": "TC_006",
        "description": "Short password rejected by API",
        "data_factory": lambda: {
            "f_name": "Alison",
            "l_name": "John",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("weak"),
            "password": "ejjjj"
        },
        "expected_status": 422,
        "expected_success": False,
        "expected_message": "Validation failed",
        "tags": ["negative", "validation", "password"]
    }
]

# ============================================
# TEST DATA HELPERS
# ============================================

def get_test_cases_by_tag(tag):
    return [tc for tc in ARTISAN_REG_TEST_CASES if tag in tc.get("tags", [])]

def get_smoke_tests():
    return [tc for tc in ARTISAN_REG_TEST_CASES if "smoke" in tc.get("tags", []) and not tc.get("skip", False)]

def get_positive_tests():
    return [tc for tc in ARTISAN_REG_TEST_CASES if "positive" in tc.get("tags", []) and not tc.get("skip", False)]

def get_negative_tests():
    return [tc for tc in ARTISAN_REG_TEST_CASES if "negative" in tc.get("tags", []) and not tc.get("skip", False)]

def get_security_tests():
    return [tc for tc in ARTISAN_REG_TEST_CASES if "security" in tc.get("tags", [])]

def get_validation_tests():
    return [tc for tc in ARTISAN_REG_TEST_CASES if "validation" in tc.get("tags", [])]

def get_critical_tests():
    return [tc for tc in ARTISAN_REG_TEST_CASES if "critical" in tc.get("tags", [])]

def get_duplicate_tests():
    return [tc for tc in ARTISAN_REG_TEST_CASES if "duplicate" in tc.get("tags", []) and not tc.get("skip", False)]

def get_optional_field_tests():
    return [tc for tc in ARTISAN_REG_TEST_CASES if "optional_fields" in tc.get("tags", [])]

def get_required_field_tests():
    return [tc for tc in ARTISAN_REG_TEST_CASES if "required_fields" in tc.get("tags", [])]

# ============================================
# TEST DATA SETS
# ============================================

SMOKE_TESTS = get_smoke_tests()
POSITIVE_TESTS = get_positive_tests()
NEGATIVE_TESTS = get_negative_tests()
VALIDATION_TESTS = get_validation_tests()
SECURITY_TESTS = get_security_tests()
CRITICAL_TESTS = get_critical_tests()
DUPLICATE_TESTS = get_duplicate_tests()
OPTIONAL_FIELD_TESTS = get_optional_field_tests()
REQUIRED_FIELD_TESTS = get_required_field_tests()
