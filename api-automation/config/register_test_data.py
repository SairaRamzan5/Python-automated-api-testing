# # """Test data for registration API tests - FINAL WORKING VERSION WITH CORRECT PHONE FORMAT"""

# # import uuid
# # import time

# # def generate_unique_email(base="artisan"):
# #     """Generate a unique email for testing"""
# #     timestamp = int(time.time() * 1000)
# #     return f"{base}_{timestamp}_{uuid.uuid4().hex[:4]}@test.com"

# # def generate_unique_phone():
# #     """Generate a unique phone number for testing - 13 DIGITS FOR BANGLADESH"""
# #     timestamp = int(time.time() * 1000)
# #     # Generate 8 random digits for the phone number
# #     # +88017 (5 digits) + XXXXXXXX (8 digits) = 13 digits total
# #     import random
# #     phone_suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
# #     return f"+88017{phone_suffix}"

# # # ============================================
# # # ARTISAN REGISTRATION TEST DATA - USING LAMBDAS
# # # ============================================

# # ARTISAN_REG_TEST_CASES = [
# #     # TC_Artisan_Reg_01: Valid Artisan Registration
# #     {
# #         "test_id": "TC_Artisan_Reg_01",
# #         "description": "Valid artisan registration with all required fields",
# #         "data_factory": lambda: {
# #             "f_name": "Artisan",
# #             "l_name": "Test",
# #             "phone": generate_unique_phone(),  # Use the function
# #             "email": generate_unique_email("artisan"),
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 201,
# #         "expected_success": True,
# #         "expected_message": "Register Successfully",
# #         "should_have_user_data": True,
# #         "expected_user_fields": ["id", "f_name", "l_name", "phone", "email", "phone_verified", "email_verified"],
# #         "tags": ["smoke", "positive", "critical"]
# #     },
    
# #     # TC_Artisan_Reg_02: Duplicate Email Registration
# #     {
# #         "test_id": "TC_Artisan_Reg_02",
# #         "description": "Registration with duplicate email",
# #         "data_factory": lambda: {
# #             "f_name": "Duplicate",
# #             "l_name": "User",
# #             "phone": generate_unique_phone(),
# #             "email": "existing@example.com",  # Must exist in DB
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 409,
# #         "expected_success": False,
# #         "expected_message": "User already exists",
# #         "skip": True,
# #         "tags": ["negative", "duplicate"]
# #     },
    
# #     # TC_Artisan_Reg_03: Duplicate Phone Registration
# #     {
# #         "test_id": "TC_Artisan_Reg_03",
# #         "description": "Registration with duplicate phone",
# #         "data_factory": lambda: {
# #             "f_name": "Duplicate",
# #             "l_name": "Phone",
# #             "phone": "+8801712345678",  # Must exist in DB
# #             "email": generate_unique_email("duplicate_phone"),
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 409,
# #         "expected_success": False,
# #         "expected_message": "User already exists",
# #         "skip": True,
# #         "tags": ["negative", "duplicate"]
# #     },
    
# #     # TC_Artisan_Reg_04: Invalid Email Format
# #     {
# #         "test_id": "TC_Artisan_Reg_04",
# #         "description": "Registration with invalid email format",
# #         "data_factory": lambda: {
# #             "f_name": "Invalid",
# #             "l_name": "Email",
# #             "phone": generate_unique_phone(),
# #             "email": "not-an-email",
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 422,
# #         "expected_success": False,
# #         "expected_message": "Validation failed",
# #         "expected_errors": ["email"],
# #         "tags": ["negative", "validation"]
# #     },
    
# #     # TC_Artisan_Reg_05: Weak Password
# #     {
# #         "test_id": "TC_Artisan_Reg_05",
# #         "description": "Registration with weak password",
# #         "data_factory": lambda: {
# #             "f_name": "Weak",
# #             "l_name": "Password",
# #             "phone": generate_unique_phone(),
# #             "email": generate_unique_email("weakpass"),
# #             "password": "123",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 422,
# #         "expected_success": False,
# #         "expected_message": "Validation failed",
# #         "expected_errors": ["password"],
# #         "tags": ["negative", "validation"]
# #     },
    
# #     # TC_Artisan_Reg_06: Missing Required Field - f_name
# #     {
# #         "test_id": "TC_Artisan_Reg_06",
# #         "description": "Registration missing first name",
# #         "data_factory": lambda: {
# #             "l_name": "Test",
# #             "phone": generate_unique_phone(),
# #             "email": generate_unique_email("missing_fname"),
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 422,
# #         "expected_success": False,
# #         "expected_message": "Validation failed",
# #         "expected_errors": ["f_name"],
# #         "tags": ["negative", "validation"]
# #     },
    
# #     # TC_Artisan_Reg_07: Missing Field - l_name (Optional)
# #     {
# #         "test_id": "TC_Artisan_Reg_07",
# #         "description": "Registration missing last name",
# #         "data_factory": lambda: {
# #             "f_name": "Test",
# #             "phone": generate_unique_phone(),
# #             "email": generate_unique_email("missing_lname"),
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 201,
# #         "expected_success": True,
# #         "expected_message": "Register Successfully",
# #         "should_have_user_data": True,
# #         "tags": ["positive"]
# #     },
    
# #     # TC_Artisan_Reg_08: Missing Field - email (Optional)
# #     {
# #         "test_id": "TC_Artisan_Reg_08",
# #         "description": "Registration missing email",
# #         "data_factory": lambda: {
# #             "f_name": "No",
# #             "l_name": "Email",
# #             "phone": generate_unique_phone(),
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 201,
# #         "expected_success": True,
# #         "expected_message": "Register Successfully",
# #         "should_have_user_data": True,
# #         "tags": ["positive"]
# #     },
    
# #     # TC_Artisan_Reg_09: Missing Required Field - phone
# #     {
# #         "test_id": "TC_Artisan_Reg_09",
# #         "description": "Registration missing phone",
# #         "data_factory": lambda: {
# #             "f_name": "No",
# #             "l_name": "Phone",
# #             "email": generate_unique_email("missing_phone"),
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 422,
# #         "expected_success": False,
# #         "expected_message": "Validation failed",
# #         "expected_errors": ["phone"],
# #         "tags": ["negative", "validation"]
# #     },
    
# #     # TC_Artisan_Reg_10: Missing Required Field - password
# #     {
# #         "test_id": "TC_Artisan_Reg_10",
# #         "description": "Registration missing password",
# #         "data_factory": lambda: {
# #             "f_name": "No",
# #             "l_name": "Password",
# #             "phone": generate_unique_phone(),
# #             "email": generate_unique_email("missing_pass"),
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 422,
# #         "expected_success": False,
# #         "expected_message": "Validation failed",
# #         "expected_errors": ["password"],
# #         "tags": ["negative", "validation"]
# #     },
    
# #     # TC_Artisan_Reg_11: Invalid Phone Format
# #     {
# #         "test_id": "TC_Artisan_Reg_11",
# #         "description": "Registration with invalid phone format",
# #         "data_factory": lambda: {
# #             "f_name": "Invalid",
# #             "l_name": "Phone",
# #             "phone": "abc123",
# #             "email": generate_unique_email("invalid_phone"),
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 422,
# #         "expected_success": False,
# #         "expected_message": "Validation failed",
# #         "expected_errors": ["phone"],
# #         "tags": ["negative", "validation"]
# #     },
    
# #     # TC_Artisan_Reg_12: SQL Injection Attempt
# #     {
# #         "test_id": "TC_Artisan_Reg_12",
# #         "description": "Registration with SQL injection attempt",
# #         "data_factory": lambda: {
# #             "f_name": "Robert'); DROP TABLE users;--",
# #             "l_name": "Test",
# #             "phone": generate_unique_phone(),
# #             "email": generate_unique_email("sql_inject"),
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 422,
# #         "expected_success": False,
# #         "tags": ["security"]
# #     },
    
# #     # TC_Artisan_Reg_13: XSS Attempt
# #     {
# #         "test_id": "TC_Artisan_Reg_13",
# #         "description": "Registration with XSS attempt",
# #         "data_factory": lambda: {
# #             "f_name": "<script>alert('xss')</script>",
# #             "l_name": "Test",
# #             "phone": generate_unique_phone(),
# #             "email": generate_unique_email("xss"),
# #             "password": "SecurePass123!",
# #             "frontend_url": "https://uat.teresaapp.com/verify"
# #         },
# #         "expected_status": 422,
# #         "expected_success": False,
# #         "tags": ["security"]
# #     }
# # ]

# # # ============================================
# # # TEST DATA HELPERS
# # # ============================================

# # def get_test_cases_by_tag(tag, test_cases=ARTISAN_REG_TEST_CASES):
# #     """Filter test cases by tag"""
# #     return [tc for tc in test_cases if tag in tc.get("tags", [])]

# # def get_smoke_tests():
# #     """Get smoke test cases"""
# #     return [tc for tc in ARTISAN_REG_TEST_CASES if "smoke" in tc.get("tags", []) and not tc.get("skip", False)]

# # def get_positive_tests():
# #     """Get positive test cases"""
# #     return [tc for tc in ARTISAN_REG_TEST_CASES if "positive" in tc.get("tags", []) and not tc.get("skip", False)]

# # def get_negative_tests():
# #     """Get negative test cases (excluding skipped)"""
# #     return [tc for tc in ARTISAN_REG_TEST_CASES if "negative" in tc.get("tags", []) and not tc.get("skip", False)]

# # def get_security_tests():
# #     """Get security test cases"""
# #     return [tc for tc in ARTISAN_REG_TEST_CASES if "security" in tc.get("tags", []) and not tc.get("skip", False)]

# # def get_validation_tests():
# #     """Get validation test cases"""
# #     return [tc for tc in ARTISAN_REG_TEST_CASES if "validation" in tc.get("tags", []) and not tc.get("skip", False)]

# # def get_critical_tests():
# #     """Get critical test cases"""
# #     return [tc for tc in ARTISAN_REG_TEST_CASES if "critical" in tc.get("tags", []) and not tc.get("skip", False)]

# # def get_duplicate_tests():
# #     """Get duplicate test cases (excluding skipped)"""
# #     return [tc for tc in ARTISAN_REG_TEST_CASES if "duplicate" in tc.get("tags", []) and not tc.get("skip", False)]

# # # ============================================
# # # TEST DATA SETS
# # # ============================================

# # SMOKE_TESTS = get_smoke_tests()
# # POSITIVE_TESTS = get_positive_tests()
# # NEGATIVE_TESTS = get_negative_tests()
# # VALIDATION_TESTS = get_validation_tests()
# # SECURITY_TESTS = get_security_tests()
# # CRITICAL_TESTS = get_critical_tests()
# # DUPLICATE_TESTS = get_duplicate_tests()

# """Test data for registration API tests - FINAL WORKING VERSION WITH CORRECT PHONE FORMAT"""

# import uuid
# import time
# import random  # Added import at top level

# def generate_unique_email(base="artisan"):
#     """Generate a unique email for testing"""
#     timestamp = int(time.time() * 1000)
#     return f"{base}_{timestamp}_{uuid.uuid4().hex[:4]}@test.com"

# def generate_unique_phone():
#     """Generate a unique phone number for testing - 13 DIGITS FOR BANGLADESH"""
#     # Generate 8 random digits for the phone number
#     # +88017 (5 digits) + XXXXXXXX (8 digits) = 13 digits total
#     phone_suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
#     return f"+88017{phone_suffix}"

# # ============================================
# # ARTISAN REGISTRATION TEST DATA - USING LAMBDAS
# # ============================================

# ARTISAN_REG_TEST_CASES = [
#     # TC_Artisan_Reg_01: Valid Artisan Registration
#     {
#         "test_id": "TC_Artisan_Reg_01",
#         "description": "Valid artisan registration with all required fields",
#         "data_factory": lambda: {
#             "f_name": "Artisan",
#             "l_name": "Test",
#             "phone": generate_unique_phone(),  # Use the function
#             "email": generate_unique_email("artisan"),
#             "password": "SecurePass123!"
#         },
#         "expected_status": 201,
#         "expected_success": True,
#         "expected_message": "Register Successfully",
#         "should_have_user_data": True,
#         "expected_user_fields": ["id", "phone", "email", "phone_verified", "email_verified"],
#         "tags": ["smoke", "positive", "critical"]
#     },
    
#     # TC_Artisan_Reg_02: Duplicate Email Registration
#     {
#         "test_id": "TC_Artisan_Reg_02",
#         "description": "Registration with duplicate email",
#         "data_factory": lambda: {
#             "f_name": "Duplicate",
#             "l_name": "User",
#             "phone": generate_unique_phone(),
#             "email": "existing@example.com",  # Must exist in DB
#             "password": "SecurePass123!"
#         },
#         "expected_status": 409,
#         "expected_success": False,
#         "expected_message": "User already exists",
#         "skip": True,
#         "tags": ["negative", "duplicate"]
#     },
    
#     # TC_Artisan_Reg_03: Duplicate Phone Registration
#     {
#         "test_id": "TC_Artisan_Reg_03",
#         "description": "Registration with duplicate phone",
#         "data_factory": lambda: {
#             "f_name": "Duplicate",
#             "l_name": "Phone",
#             "phone": "+8801712345678",  # Must exist in DB
#             "email": generate_unique_email("duplicate_phone"),
#             "password": "SecurePass123!"
#         },
#         "expected_status": 409,
#         "expected_success": False,
#         "expected_message": "User already exists",
#         "skip": True,
#         "tags": ["negative", "duplicate"]
#     },
    
#     # TC_Artisan_Reg_04: Invalid Email Format
#     {
#         "test_id": "TC_Artisan_Reg_04",
#         "description": "Registration with invalid email format",
#         "data_factory": lambda: {
#             "f_name": "Invalid",
#             "l_name": "Email",
#             "phone": generate_unique_phone(),
#             "email": "not-an-email",
#             "password": "SecurePass123!"
#         },
#         "expected_status": 422,
#         "expected_success": False,
#         "expected_message": "Validation failed",
#         "expected_errors": ["email"],
#         "tags": ["negative", "validation"]
#     },
    
#     # TC_Artisan_Reg_05: Weak Password
#     {
#         "test_id": "TC_Artisan_Reg_05",
#         "description": "Registration with weak password",
#         "data_factory": lambda: {
#             "f_name": "Weak",
#             "l_name": "Password",
#             "phone": generate_unique_phone(),
#             "email": generate_unique_email("weakpass"),
#             "password": "123"
#         },
#         "expected_status": 422,
#         "expected_success": False,
#         "expected_message": "Validation failed",
#         "expected_errors": ["password"],
#         "tags": ["negative", "validation"]
#     },
    
#     # TC_Artisan_Reg_06: Missing Optional Field - f_name
#     {
#         "test_id": "TC_Artisan_Reg_06",
#         "description": "Registration missing first name",
#         "data_factory": lambda: {
#             "l_name": "Test",
#             "phone": generate_unique_phone(),
#             "email": generate_unique_email("missing_fname"),
#             "password": "SecurePass123!"
#         },
#         "expected_status": 201,
#         "expected_success": True,
#         "expected_message": "Register Successfully",
#         "expected_user_fields": ["id", "phone", "email", "phone_verified", "email_verified"],
#         "tags": ["positive", "validation"]
#     },
    
#     # TC_Artisan_Reg_07: Missing Field - l_name (Optional)
#     {
#         "test_id": "TC_Artisan_Reg_07",
#         "description": "Registration missing last name",
#         "data_factory": lambda: {
#             "f_name": "Test",
#             "phone": generate_unique_phone(),
#             "email": generate_unique_email("missing_lname"),
#             "password": "SecurePass123!"
#         },
#         "expected_status": 201,
#         "expected_success": True,
#         "expected_message": "Register Successfully",
#         "should_have_user_data": True,
#         "tags": ["positive"]
#     },
    
#     # TC_Artisan_Reg_08: Missing Field - email (Optional)
#     {
#         "test_id": "TC_Artisan_Reg_08",
#         "description": "Registration missing email",
#         "data_factory": lambda: {
#             "f_name": "No",
#             "l_name": "Email",
#             "phone": generate_unique_phone(),
#             "password": "SecurePass123!"
#         },
#         "expected_status": 201,
#         "expected_success": True,
#         "expected_message": "Register Successfully",
#         "should_have_user_data": True,
#         "tags": ["positive"]
#     },
    
#     # TC_Artisan_Reg_09: Missing Required Field - phone
#     {
#         "test_id": "TC_Artisan_Reg_09",
#         "description": "Registration missing phone",
#         "data_factory": lambda: {
#             "f_name": "No",
#             "l_name": "Phone",
#             "email": generate_unique_email("missing_phone"),
#             "password": "SecurePass123!"
#         },
#         "expected_status": 422,
#         "expected_success": False,
#         "expected_message": "Validation failed",
#         "expected_errors": ["phone"],
#         "tags": ["negative", "validation"]
#     },
    
#     # TC_Artisan_Reg_10: Missing Required Field - password
#     {
#         "test_id": "TC_Artisan_Reg_10",
#         "description": "Registration missing password",
#         "data_factory": lambda: {
#             "f_name": "No",
#             "l_name": "Password",
#             "phone": generate_unique_phone(),
#             "email": generate_unique_email("missing_pass")
#         },
#         "expected_status": 422,
#         "expected_success": False,
#         "expected_message": "Validation failed",
#         "expected_errors": ["password"],
#         "tags": ["negative", "validation"]
#     },
    
#     # TC_Artisan_Reg_11: Invalid Phone Format
#     {
#         "test_id": "TC_Artisan_Reg_11",
#         "description": "Registration with invalid phone format",
#         "data_factory": lambda: {
#             "f_name": "Invalid",
#             "l_name": "Phone",
#             "phone": "abc123",
#             "email": generate_unique_email("invalid_phone"),
#             "password": "SecurePass123!"
#         },
#         "expected_status": 422,
#         "expected_success": False,
#         "expected_message": "Validation failed",
#         "expected_errors": ["phone"],
#         "tags": ["negative", "validation"]
#     },
    
#     # TC_Artisan_Reg_12: SQL Injection Attempt
#     {
#         "test_id": "TC_Artisan_Reg_12",
#         "description": "Registration with SQL injection attempt",
#         "data_factory": lambda: {
#             "f_name": "Robert'); DROP TABLE users;--",
#             "l_name": "Test",
#             "phone": generate_unique_phone(),
#             "email": generate_unique_email("sql_inject"),
#             "password": "SecurePass123!"
#         },
#         "expected_status": 422,
#         "expected_success": False,
#         "tags": ["security"]
#     },
    
#     # TC_Artisan_Reg_13: XSS Attempt
#     {
#         "test_id": "TC_Artisan_Reg_13",
#         "description": "Registration with XSS attempt",
#         "data_factory": lambda: {
#             "f_name": "<script>alert('xss')</script>",
#             "l_name": "Test",
#             "phone": generate_unique_phone(),
#             "email": generate_unique_email("xss"),
#             "password": "SecurePass123!"
#         },
#         "expected_status": 422,
#         "expected_success": False,
#         "tags": ["security"]
#     }
# ]

# # ============================================
# # TEST DATA HELPERS
# # ============================================

# def get_test_cases_by_tag(tag, test_cases=ARTISAN_REG_TEST_CASES):
#     """Filter test cases by tag"""
#     return [tc for tc in test_cases if tag in tc.get("tags", [])]

# def get_smoke_tests():
#     """Get smoke test cases"""
#     return [tc for tc in ARTISAN_REG_TEST_CASES if "smoke" in tc.get("tags", []) and not tc.get("skip", False)]

# def get_positive_tests():
#     """Get positive test cases"""
#     return [tc for tc in ARTISAN_REG_TEST_CASES if "positive" in tc.get("tags", []) and not tc.get("skip", False)]

# def get_negative_tests():
#     """Get negative test cases (excluding skipped)"""
#     return [tc for tc in ARTISAN_REG_TEST_CASES if "negative" in tc.get("tags", []) and not tc.get("skip", False)]

# def get_security_tests():
#     """Get security test cases"""
#     return [tc for tc in ARTISAN_REG_TEST_CASES if "security" in tc.get("tags", []) and not tc.get("skip", False)]

# def get_validation_tests():
#     """Get validation test cases"""
#     return [tc for tc in ARTISAN_REG_TEST_CASES if "validation" in tc.get("tags", []) and not tc.get("skip", False)]

# def get_critical_tests():
#     """Get critical test cases"""
#     return [tc for tc in ARTISAN_REG_TEST_CASES if "critical" in tc.get("tags", []) and not tc.get("skip", False)]

# def get_duplicate_tests():
#     """Get duplicate test cases (excluding skipped)"""
#     return [tc for tc in ARTISAN_REG_TEST_CASES if "duplicate" in tc.get("tags", []) and not tc.get("skip", False)]

# # ============================================
# # TEST DATA SETS
# # ============================================

# SMOKE_TESTS = get_smoke_tests()
# POSITIVE_TESTS = get_positive_tests()
# NEGATIVE_TESTS = get_negative_tests()
# VALIDATION_TESTS = get_validation_tests()
# SECURITY_TESTS = get_security_tests()
# CRITICAL_TESTS = get_critical_tests()
# DUPLICATE_TESTS = get_duplicate_tests()

"""Test data for registration API tests - CORRECTED VERSION

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

def generate_unique_email(base="artisan"):
    """Generate a unique email for testing"""
    timestamp = int(time.time() * 1000)
    return f"{base}_{timestamp}_{uuid.uuid4().hex[:4]}@test.com"

def generate_unique_phone():
    """Generate a unique phone number for testing - 13 DIGITS FOR BANGLADESH"""
    # Generate 8 random digits for the phone number
    # +88017 (5 digits) + XXXXXXXX (8 digits) = 13 digits total
    phone_suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return f"+88017{phone_suffix}"

# ============================================
# ARTISAN REGISTRATION TEST DATA
# ============================================

ARTISAN_REG_TEST_CASES = [
    # TC_Artisan_Reg_01: Valid Registration with All Fields
    {
        "test_id": "TC_Artisan_Reg_01",
        "description": "Valid artisan registration with all fields (required + optional)",
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
            "email": "existing@example.com",  # Must exist in DB
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
            "phone": "+8801712345678",  # Must exist in DB
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
        "description": "Registration with invalid email format",
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
        "description": "Registration with weak password",
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
    
    # TC_Artisan_Reg_06: Missing Optional Field - f_name ✅ CORRECT
    {
        "test_id": "TC_Artisan_Reg_06",
        "description": "Registration without first name (optional field)",
        "data_factory": lambda: {
            "l_name": "Test",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("no_fname"),
            "password": "SecurePass123!"
        },
        "expected_status": 201,  # ✅ Should succeed - f_name is optional
        "expected_success": True,
        "expected_message": "Register Successfully",
        "should_have_user_data": True,
        "expected_user_fields": ["id", "phone", "email", "phone_verified", "email_verified"],
        "tags": ["positive", "optional_fields"]
    },
    
    # TC_Artisan_Reg_07: Missing Optional Field - l_name ✅ CORRECT
    {
        "test_id": "TC_Artisan_Reg_07",
        "description": "Registration without last name (optional field)",
        "data_factory": lambda: {
            "f_name": "Test",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("no_lname"),
            "password": "SecurePass123!"
        },
        "expected_status": 201,  # ✅ Should succeed - l_name is optional
        "expected_success": True,
        "expected_message": "Register Successfully",
        "should_have_user_data": True,
        "tags": ["positive", "optional_fields"]
    },
    
    # TC_Artisan_Reg_08: Missing Optional Field - email ✅ CORRECT
    {
        "test_id": "TC_Artisan_Reg_08",
        "description": "Registration without email (optional field)",
        "data_factory": lambda: {
            "f_name": "No",
            "l_name": "Email",
            "phone": generate_unique_phone(),
            "password": "SecurePass123!"
        },
        "expected_status": 201,  # ✅ Should succeed - email is optional
        "expected_success": True,
        "expected_message": "Register Successfully",
        "should_have_user_data": True,
        "tags": ["positive", "optional_fields"]
    },
    
    # TC_Artisan_Reg_09: Missing REQUIRED Field - phone ✅ CORRECT
    {
        "test_id": "TC_Artisan_Reg_09",
        "description": "Registration without phone (required field)",
        "data_factory": lambda: {
            "f_name": "No",
            "l_name": "Phone",
            "email": generate_unique_email("no_phone"),
            "password": "SecurePass123!"
        },
        "expected_status": 422,  # ✅ Should fail - phone is required
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": ["phone"],
        "tags": ["negative", "validation", "required_fields"]
    },
    
    # TC_Artisan_Reg_10: Missing REQUIRED Field - password ✅ CORRECT
    {
        "test_id": "TC_Artisan_Reg_10",
        "description": "Registration without password (required field)",
        "data_factory": lambda: {
            "f_name": "No",
            "l_name": "Password",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("no_pass")
        },
        "expected_status": 422,  # ✅ Should fail - password is required
        "expected_success": False,
        "expected_message": "Validation failed",
        "expected_errors": ["password"],
        "tags": ["negative", "validation", "required_fields"]
    },
    
    # TC_Artisan_Reg_11: Invalid Phone Format
    {
        "test_id": "TC_Artisan_Reg_11",
        "description": "Registration with invalid phone format",
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
    
    # TC_Artisan_Reg_12: Only Required Fields (Minimal Valid Registration)
    {
        "test_id": "TC_Artisan_Reg_12",
        "description": "Registration with only required fields (phone + password)",
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
    
    # TC_Artisan_Reg_13: SQL Injection Attempt
    {
        "test_id": "TC_Artisan_Reg_13",
        "description": "Registration with SQL injection attempt",
        "data_factory": lambda: {
            "f_name": "Robert'); DROP TABLE users;--",
            "l_name": "Test",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("sql_inject"),
            "password": "SecurePass123!"
        },
        "expected_status": 422,
        "expected_success": False,
        "tags": ["security"]
    },
    
    # TC_Artisan_Reg_14: XSS Attempt
    {
        "test_id": "TC_Artisan_Reg_14",
        "description": "Registration with XSS attempt",
        "data_factory": lambda: {
            "f_name": "<script>alert('xss')</script>",
            "l_name": "Test",
            "phone": generate_unique_phone(),
            "email": generate_unique_email("xss"),
            "password": "SecurePass123!"
        },
        "expected_status": 422,
        "expected_success": False,
        "tags": ["security"]
    }
]

# ============================================
# TEST DATA HELPERS
# ============================================

def get_test_cases_by_tag(tag, test_cases=ARTISAN_REG_TEST_CASES):
    """Filter test cases by tag"""
    return [tc for tc in test_cases if tag in tc.get("tags", [])]

def get_smoke_tests():
    """Get smoke test cases"""
    return [tc for tc in ARTISAN_REG_TEST_CASES if "smoke" in tc.get("tags", []) and not tc.get("skip", False)]

def get_positive_tests():
    """Get positive test cases"""
    return [tc for tc in ARTISAN_REG_TEST_CASES if "positive" in tc.get("tags", []) and not tc.get("skip", False)]

def get_negative_tests():
    """Get negative test cases (excluding skipped)"""
    return [tc for tc in ARTISAN_REG_TEST_CASES if "negative" in tc.get("tags", []) and not tc.get("skip", False)]

def get_security_tests():
    """Get security test cases"""
    return [tc for tc in ARTISAN_REG_TEST_CASES if "security" in tc.get("tags", []) and not tc.get("skip", False)]

def get_validation_tests():
    """Get validation test cases"""
    return [tc for tc in ARTISAN_REG_TEST_CASES if "validation" in tc.get("tags", []) and not tc.get("skip", False)]

def get_critical_tests():
    """Get critical test cases"""
    return [tc for tc in ARTISAN_REG_TEST_CASES if "critical" in tc.get("tags", []) and not tc.get("skip", False)]

def get_duplicate_tests():
    """Get duplicate test cases (excluding skipped)"""
    return [tc for tc in ARTISAN_REG_TEST_CASES if "duplicate" in tc.get("tags", []) and not tc.get("skip", False)]

def get_optional_field_tests():
    """Get tests for optional fields"""
    return [tc for tc in ARTISAN_REG_TEST_CASES if "optional_fields" in tc.get("tags", []) and not tc.get("skip", False)]

def get_required_field_tests():
    """Get tests for required fields"""
    return [tc for tc in ARTISAN_REG_TEST_CASES if "required_fields" in tc.get("tags", []) and not tc.get("skip", False)]

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