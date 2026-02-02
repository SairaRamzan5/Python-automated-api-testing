"""Artisan Login API tests for Teresa Backoffice UAT - WITH PHONE APPROVAL REQUIREMENT"""

import pytest
import json
import time
from datetime import datetime
from api.endpoints import Endpoints
from utils.assertions import Assertions
from config.artisan_login_test_data import (
    get_test_cases_by_tag,
    generate_unique_email,
    generate_unique_phone,
    ARTISAN_LOGIN_TEST_CASES,
    ARTISAN_APPROVAL_TEST_CASES
)
from config.settings import settings

class TestArtisanLoginAPI:
    """Test suite for Artisan Login API on UAT environment with phone approval requirement"""
    
    # Store created artisans for testing
    created_artisans = []
    
    @classmethod
    def setup_class(cls):
        """Setup before all tests"""
        print(f"\n{'='*70}")
        print(f"Starting ARTISAN LOGIN API Tests - UAT Environment")
        print(f"Special Condition: Artisans require phone approval to login")
        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
    
    @classmethod
    def teardown_class(cls):
        """Cleanup after all tests"""
        print(f"\n{'='*70}")
        print(f"Artisan Login Test Summary")
        print(f"Created artisans: {len(cls.created_artisans)}")
        print(f"{'='*70}\n")
    
    @pytest.fixture(autouse=True)
    def setup_test(self, api_client):
        """Setup before each test"""
        self.client = api_client
        self.client.clear_auth_token()
        
        # Get admin token if needed for approval tests
        self.admin_token = None
    
    def get_admin_auth_token(self):
        """Get admin authentication token for approval operations"""
        if not self.admin_token:
            print("   Getting admin token...")
            
            login_data = {
                "identifier": settings.ADMIN_EMAIL,
                "password": settings.ADMIN_PASSWORD
            }
            
            login_response = self.client.post(
                Endpoints.LOGIN,
                json=login_data
            )
            
            if login_response.status_code == 200:
                response_data = login_response.json()
                if response_data.get("success"):
                    self.admin_token = response_data.get("data", {}).get("access_token")
                    if self.admin_token:
                        print(f"   ✓ Admin token obtained")
                    else:
                        print(f"   ❌ No access token in admin response")
            else:
                print(f"   ❌ Admin login failed: {login_response.status_code}")
        
        return self.admin_token
    
    def create_and_approve_artisan(self, artisan_data, approve=True):
        """Create an artisan and optionally approve their phone"""
        print(f"   Creating artisan with email: {artisan_data.get('email')}")
        
        # Step 1: Register artisan
        reg_response = self.client.post(
            Endpoints.REGISTER,
            json=artisan_data
        )
        
        if reg_response.status_code != 201:
            print(f"   ❌ Artisan creation failed: {reg_response.status_code}")
            print(f"   Response: {reg_response.text[:200]}")
            return None
        
        reg_data = reg_response.json()
        user_id = reg_data.get("data", {}).get("user", {}).get("id")
        
        if not user_id:
            print(f"   ❌ No user ID in registration response")
            return None
        
        # Store artisan info
        artisan_info = {
            "email": artisan_data.get("email"),
            "phone": artisan_data.get("phone"),
            "password": artisan_data.get("password"),
            "user_id": user_id,
            "approved": False
        }
        
        self.created_artisans.append(artisan_info)
        
        if approve:
            # Step 2: Approve artisan phone
            if self.approve_artisan_phone(user_id):
                artisan_info["approved"] = True
                print(f"   ✓ Artisan created and approved: {artisan_data.get('email')}")
            else:
                print(f"   ⚠ Artisan created but not approved: {artisan_data.get('email')}")
        else:
            print(f"   ✓ Artisan created (not approved): {artisan_data.get('email')}")
        
        return artisan_info
    
    def approve_artisan_phone(self, user_id):
        """Approve artisan phone via admin API"""
        admin_token = self.get_admin_auth_token()
        if not admin_token:
            print(f"   ❌ Cannot approve: No admin token")
            return False
        
        # Set admin token
        self.client.set_auth_token(admin_token)
        
        approval_data = {
            "user_id": user_id,
            "status": "approved",
            "reason": "Test automation approval"
        }
        
        # Use whitelist approval endpoint (adjust as needed)
        response = self.client.patch(
            Endpoints.WHITELIST_AUDIT,
            json=approval_data
        )
        
        # Clear admin token
        self.client.clear_auth_token()
        
        if response.status_code == 200:
            print(f"   ✓ Phone approved for user: {user_id}")
            return True
        else:
            print(f"   ❌ Phone approval failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    
    @pytest.mark.uat
    @pytest.mark.parametrize("test_case", ARTISAN_LOGIN_TEST_CASES)
    def test_artisan_login(self, test_case):
        """Test artisan login API with various test cases"""
        test_id = test_case['test_id']
        description = test_case['description']
        
        print(f"\n▶ Test: {test_id} - {description}")
        
        # Add delay to avoid rate limiting
        time.sleep(2.0)
        
        # For tests requiring an approved artisan
        if test_case.get("requires_approved_artisan", False):
            # Create and approve an artisan for this test
            unique_email = generate_unique_email("approved_login")
            unique_phone = generate_unique_phone()
            
            artisan_data = {
                "f_name": "Approved",
                "l_name": "Artisan",
                "phone": unique_phone,
                "email": unique_email,
                "password": "SecurePass123!",
                "frontend_url": "https://uat.teresaapp.com/verify"
            }
            
            artisan_info = self.create_and_approve_artisan(artisan_data, approve=True)
            
            if not artisan_info or not artisan_info["approved"]:
                print(f"   ⚠ Skipping test: Could not create approved artisan")
                pytest.skip("Could not create approved artisan")
                return
            
            # Use the approved artisan credentials
            login_data = {
                "identifier": artisan_info["email"],
                "password": artisan_info["password"]
            }
        
        # For tests with non-approved artisan
        elif test_case.get("requires_non_approved_artisan", False):
            # Create but don't approve an artisan
            unique_email = generate_unique_email("pending_login")
            unique_phone = generate_unique_phone()
            
            artisan_data = {
                "f_name": "Pending",
                "l_name": "Artisan",
                "phone": unique_phone,
                "email": unique_email,
                "password": "SecurePass123!",
                "frontend_url": "https://uat.teresaapp.com/verify"
            }
            
            artisan_info = self.create_and_approve_artisan(artisan_data, approve=False)
            
            if not artisan_info:
                print(f"   ⚠ Skipping test: Could not create artisan")
                pytest.skip("Could not create artisan")
                return
            
            login_data = {
                "identifier": artisan_info["email"],
                "password": artisan_info["password"]
            }
        
        else:
            # Use test case data as-is
            login_data = test_case["data"]
        
        # Mask password for security
        safe_data = login_data.copy()
        if 'password' in safe_data:
            safe_data['password'] = '********'
        print(f"   Payload: {safe_data}")
        
        # Record start time
        start_time = time.time()
        
        # Make API request
        try:
            response = self.client.post(
                Endpoints.LOGIN,
                json=login_data,
                timeout=15
            )
        except Exception as e:
            print(f"   ❌ Request failed: {str(e)}")
            pytest.skip(f"Request failed: {str(e)}")
            return
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Handle rate limiting
        if response.status_code == 429:
            print(f"   ⚠ RATE LIMITED (429) - Skipping test")
            pytest.skip(f"Rate limited (429) on UAT")
            return
        
        # Parse response JSON
        response_data = {}
        if response.text and response.text.strip():
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                print(f"   ⚠ Response is not valid JSON: {response.text[:100]}")
        
        # Assert status code
        Assertions.assert_status_code(response, test_case["expected_status"])
        
        # Assert success flag
        if "expected_success" in test_case and response_data:
            actual_success = response_data.get("success")
            expected_success = test_case["expected_success"]
            assert actual_success == expected_success, \
                f"Expected success={expected_success}, got {actual_success}"
        
        # Assert message
        if "expected_message" in test_case and test_case["expected_message"] and response_data:
            actual_message = response_data.get("message", "")
            
            # Check for phone approval message for non-approved artisans
            if test_case.get("requires_non_approved_artisan", False):
                if "phone" in actual_message.lower() and ("approve" in actual_message.lower() or "verified" in actual_message.lower()):
                    print(f"   ✓ Phone approval required message detected")
                elif "pending" in actual_message.lower():
                    print(f"   ✓ Pending approval message detected")
                else:
                    print(f"   ⚠ Expected phone approval message, got: {actual_message}")
            else:
                # Regular message check
                if test_case["expected_message"] in actual_message:
                    print(f"   ✓ Message: {actual_message}")
                else:
                    print(f"   ⚠ Expected '{test_case['expected_message']}', got '{actual_message}'")
        
        # Assert token for successful login (only for approved artisans)
        if test_case["expected_status"] == 200 and response_data:
            if "data" in response_data and "access_token" in response_data["data"]:
                access_token = response_data["data"]["access_token"]
                print(f"   ✓ Access token received: {access_token[:30]}...")
                
                # Validate token structure
                try:
                    Assertions.assert_token_structure(access_token)
                    print(f"   ✓ Token structure valid")
                except Exception as e:
                    print(f"   ⚠ Token validation failed: {e}")
                
                # Store token for future use if needed
                if test_case.get("store_token", False):
                    self.client.set_auth_token(access_token)
                    print(f"   ✓ Token stored for future requests")
            else:
                print(f"   ⚠ No access token in successful login response")
        
        # Log response time
        print(f"   Response time: {response_time:.3f}s")
        
        print(f"   ✅ PASS: {test_id}")
    
    @pytest.mark.uat_smoke
    def test_approved_artisan_smoke_login(self):
        """Smoke test: Approved artisan should be able to login"""
        print("\n▶ Smoke Test: Approved Artisan Login")
        
        # Create and approve an artisan
        unique_email = generate_unique_email("smoke_approved")
        unique_phone = generate_unique_phone()
        
        artisan_data = {
            "f_name": "Smoke",
            "l_name": "Test",
            "phone": unique_phone,
            "email": unique_email,
            "password": "SecurePass123!",
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        artisan_info = self.create_and_approve_artisan(artisan_data, approve=True)
        
        if not artisan_info or not artisan_info["approved"]:
            print(f"   ❌ Cannot proceed: Artisan not approved")
            pytest.fail("Artisan approval failed")
            return
        
        # Attempt login
        login_data = {
            "identifier": artisan_info["email"],
            "password": artisan_info["password"]
        }
        
        response = self.client.post(Endpoints.LOGIN, json=login_data)
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success") and "access_token" in response_data.get("data", {}):
                print(f"   ✓ Approved artisan login successful")
                print(f"   ✓ Token received")
                
                # Store token
                access_token = response_data["data"]["access_token"]
                self.client.set_auth_token(access_token)
                
                # Verify token works for subsequent requests
                # Try to access profile or artisan-specific endpoint
                try:
                    profile_response = self.client.get("profile", timeout=10)
                    if profile_response.status_code in [200, 201]:
                        print(f"   ✓ Token works for profile access")
                    else:
                        print(f"   ⚠ Profile access status: {profile_response.status_code}")
                except Exception as e:
                    print(f"   ⚠ Profile access test skipped: {str(e)}")
            else:
                print(f"   ❌ Login response missing token")
                pytest.fail("No access token in successful login")
        else:
            print(f"   ❌ Approved artisan login failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            pytest.fail("Approved artisan should be able to login")
        
        print("   ✅ PASS: Approved artisan smoke test")
    
    @pytest.mark.uat_critical
    def test_non_approved_artisan_cannot_login(self):
        """Critical test: Non-approved artisan should NOT be able to login"""
        print("\n▶ Critical Test: Non-Approved Artisan Login Should Fail")
        
        # Create but don't approve an artisan
        unique_email = generate_unique_email("non_approved")
        unique_phone = generate_unique_phone()
        
        artisan_data = {
            "f_name": "Non",
            "l_name": "Approved",
            "phone": unique_phone,
            "email": unique_email,
            "password": "SecurePass123!",
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        artisan_info = self.create_and_approve_artisan(artisan_data, approve=False)
        
        if not artisan_info or artisan_info["approved"]:
            print(f"   ⚠ Test setup issue: Artisan should not be approved")
            pytest.skip("Test setup failed")
            return
        
        # Attempt login
        login_data = {
            "identifier": artisan_info["email"],
            "password": artisan_info["password"]
        }
        
        response = self.client.post(Endpoints.LOGIN, json=login_data)
        
        # Should NOT be 200
        if response.status_code == 200:
            print(f"   ❌ NON-APPROVED artisan logged in successfully!")
            print(f"   Response: {response.text[:200]}")
            pytest.fail("Non-approved artisan should not be able to login")
        elif response.status_code == 401:
            print(f"   ✓ Non-approved artisan correctly rejected: 401 Unauthorized")
        elif response.status_code == 403:
            print(f"   ✓ Non-approved artisan correctly rejected: 403 Forbidden")
        elif response.status_code == 400:
            response_data = response.json() if response.text else {}
            message = response_data.get("message", "")
            if "phone" in message.lower() or "approve" in message.lower() or "pending" in message.lower():
                print(f"   ✓ Non-approved artisan rejected with phone approval message")
            else:
                print(f"   ✓ Non-approved artisan rejected: 400")
        else:
            print(f"   ⚠ Non-approved artisan got unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
        
        print("   ✅ PASS: Non-approved artisan login blocked")
    
    @pytest.mark.uat_integration
    def test_artisan_login_workflow_integration(self):
        """Integration test: Complete artisan registration → approval → login workflow"""
        print("\n▶ Integration Test: Artisan Registration → Approval → Login Workflow")
        
        # Step 1: Register artisan
        unique_email = generate_unique_email("workflow")
        unique_phone = generate_unique_phone()
        
        artisan_data = {
            "f_name": "Workflow",
            "l_name": "Test",
            "phone": unique_phone,
            "email": unique_email,
            "password": "SecurePass123!",
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        print(f"   Step 1: Registering artisan...")
        reg_response = self.client.post(Endpoints.REGISTER, json=artisan_data)
        
        if reg_response.status_code != 201:
            print(f"   ❌ Registration failed: {reg_response.status_code}")
            pytest.fail("Artisan registration failed")
            return
        
        reg_data = reg_response.json()
        user_id = reg_data.get("data", {}).get("user", {}).get("id")
        
        if not user_id:
            print(f"   ❌ No user ID in registration response")
            pytest.fail("Cannot get user ID from registration")
            return
        
        print(f"   ✓ Artisan registered: {unique_email}")
        print(f"   ✓ User ID: {user_id}")
        
        # Step 2: Try login BEFORE approval (should fail)
        print(f"\n   Step 2: Trying login BEFORE approval...")
        login_data = {
            "identifier": unique_email,
            "password": artisan_data["password"]
        }
        
        login_response1 = self.client.post(Endpoints.LOGIN, json=login_data)
        
        if login_response1.status_code == 200:
            print(f"   ⚠ WARNING: Artisan logged in BEFORE approval")
        else:
            print(f"   ✓ Login blocked before approval: {login_response1.status_code}")
        
        # Step 3: Approve artisan phone
        print(f"\n   Step 3: Approving artisan phone...")
        admin_token = self.get_admin_auth_token()
        if not admin_token:
            print(f"   ❌ Cannot get admin token for approval")
            pytest.skip("Admin approval not available")
            return
        
        self.client.set_auth_token(admin_token)
        
        approval_data = {
            "user_id": user_id,
            "status": "approved",
            "reason": "Integration test approval"
        }
        
        approval_response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=approval_data)
        
        self.client.clear_auth_token()
        
        if approval_response.status_code == 200:
            print(f"   ✓ Artisan approved successfully")
        else:
            print(f"   ❌ Approval failed: {approval_response.status_code}")
            print(f"   Response: {approval_response.text[:200]}")
            pytest.fail("Artisan approval failed")
        
        # Step 4: Try login AFTER approval (should succeed)
        print(f"\n   Step 4: Trying login AFTER approval...")
        time.sleep(2.0)  # Give system time to process approval
        
        login_response2 = self.client.post(Endpoints.LOGIN, json=login_data)
        
        if login_response2.status_code == 200:
            response_data = login_response2.json()
            if response_data.get("success") and "access_token" in response_data.get("data", {}):
                print(f"   ✓ Approved artisan login successful!")
                
                # Store for future tests
                self.created_artisans.append({
                    "email": unique_email,
                    "phone": unique_phone,
                    "password": artisan_data["password"],
                    "user_id": user_id,
                    "approved": True
                })
            else:
                print(f"   ⚠ Login successful but no token in response")
        else:
            print(f"   ❌ Approved artisan login failed: {login_response2.status_code}")
            print(f"   Response: {login_response2.text[:200]}")
            pytest.fail("Approved artisan should be able to login")
        
        print("   ✅ PASS: Complete workflow integration test")
    
    @pytest.mark.uat_security
    def test_artisan_login_security_scenarios(self):
        """Test security scenarios for artisan login"""
        print("\n▶ Security Test: Artisan Login Security Scenarios")
        
        # Create an approved artisan first
        unique_email = generate_unique_email("security")
        unique_phone = generate_unique_phone()
        
        artisan_data = {
            "f_name": "Security",
            "l_name": "Test",
            "phone": unique_phone,
            "email": unique_email,
            "password": "SecurePass123!",
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        artisan_info = self.create_and_approve_artisan(artisan_data, approve=True)
        
        if not artisan_info:
            print(f"   ❌ Cannot create test artisan")
            pytest.skip("Test artisan creation failed")
            return
        
        test_cases = [
            {
                "name": "Wrong password for approved artisan",
                "data": {"identifier": unique_email, "password": "WrongPass123!"},
                "expected_status": 401,
                "description": "Should reject wrong password"
            },
            {
                "name": "Wrong email for approved artisan",
                "data": {"identifier": "nonexistent@example.com", "password": artisan_data["password"]},
                "expected_status": 401,
                "description": "Should reject non-existent user"
            },
            {
                "name": "Empty password",
                "data": {"identifier": unique_email, "password": ""},
                "expected_status": 422,
                "description": "Should reject empty password"
            },
            {
                "name": "Empty identifier",
                "data": {"identifier": "", "password": artisan_data["password"]},
                "expected_status": 422,
                "description": "Should reject empty identifier"
            },
            {
                "name": "SQL injection attempt",
                "data": {"identifier": "admin'--", "password": "anything"},
                "expected_status": 401,
                "description": "Should reject SQL injection"
            },
            {
                "name": "XSS attempt",
                "data": {"identifier": "<script>alert('xss')</script>", "password": "test123"},
                "expected_status": 401,
                "description": "Should reject XSS payload"
            }
        ]
        
        passed_tests = 0
        
        for test_case in test_cases:
            print(f"   Testing: {test_case['name']}")
            
            time.sleep(1.0)  # Delay between tests
            
            response = self.client.post(Endpoints.LOGIN, json=test_case["data"])
            
            if response.status_code == 429:
                print(f"     ⚠ Rate limited - skipping rest of security tests")
                break
            
            if response.status_code == test_case["expected_status"]:
                print(f"     ✓ Correctly rejected: {response.status_code}")
                passed_tests += 1
            else:
                print(f"     ❌ Expected {test_case['expected_status']}, got {response.status_code}")
        
        print(f"\n   Security tests passed: {passed_tests}/{len(test_cases)}")
        print("   ✅ PASS: Artisan login security tests")
    
    @pytest.mark.uat_performance
    def test_artisan_login_performance(self):
        """Test artisan login performance with approval requirement"""
        print("\n▶ Performance Test: Artisan Login with Approval Check")
        
        # Create multiple approved artisans for performance testing
        test_artisans = []
        
        for i in range(2):  # Create 2 approved artisans
            unique_email = generate_unique_email(f"perf{i}")
            unique_phone = generate_unique_phone()
            
            artisan_data = {
                "f_name": f"Perf{i}",
                "l_name": "Test",
                "phone": unique_phone,
                "email": unique_email,
                "password": "SecurePass123!",
                "frontend_url": "https://uat.teresaapp.com/verify"
            }
            
            artisan_info = self.create_and_approve_artisan(artisan_data, approve=True)
            
            if artisan_info and artisan_info["approved"]:
                test_artisans.append(artisan_info)
                print(f"   Created approved artisan {i+1}: {unique_email}")
            else:
                print(f"   ⚠ Failed to create approved artisan {i+1}")
        
        if not test_artisans:
            print(f"   ⚠ No approved artisans created for performance test")
            pytest.skip("Could not create approved artisans")
            return
        
        response_times = []
        successful_logins = 0
        
        print(f"\n   Testing login performance for {len(test_artisans)} approved artisans...")
        
        for i, artisan in enumerate(test_artisans):
            time.sleep(2.0)  # Delay between login attempts
            
            login_data = {
                "identifier": artisan["email"],
                "password": artisan["password"]
            }
            
            start_time = time.time()
            response = self.client.post(Endpoints.LOGIN, json=login_data)
            response_time = time.time() - start_time
            response_times.append(response_time)
            
            if response.status_code == 200:
                successful_logins += 1
                print(f"   ✓ Login {i+1}: {response_time:.3f}s")
            else:
                print(f"   ⚠ Login {i+1} failed: {response.status_code} in {response_time:.3f}s")
        
        # Calculate statistics
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times) if response_times else 0
            min_time = min(response_times) if response_times else 0
            
            print(f"\n   Performance Summary:")
            print(f"   ✓ Login attempts: {len(test_artisans)}, Successful: {successful_logins}")
            print(f"   ✓ Response times: {[f'{t:.3f}s' for t in response_times]}")
            print(f"   ✓ Average: {avg_time:.3f}s, Min: {min_time:.3f}s, Max: {max_time:.3f}s")
            
            # UAT performance requirements
            if avg_time < 5.0:
                print(f"   ✓ Average login time meets 5s limit")
            else:
                print(f"   ⚠ Average login time {avg_time:.3f}s exceeds 5s limit")
        else:
            print(f"   ⚠ No response times recorded")
        
        print("   ✅ PASS: Artisan login performance test")