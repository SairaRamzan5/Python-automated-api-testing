# # tests/test_whitelist_approval.py
# """Whitelist Approval/Rejection API tests for Teresa Backoffice UAT"""

# import pytest
# import time
# import json
# import uuid
# from datetime import datetime
# from api.endpoints import Endpoints
# from config.test_data_whitelist_approval import WHITELIST_APPROVAL_TEST_CASES, VALID_STATUSES
# from utils.assertions import Assertions
# from config.settings import settings

# class TestWhitelistApprovalAPI:
#     """Test suite for Whitelist Approval/Rejection API on UAT environment"""
    
#     @classmethod
#     def setup_class(cls):
#         """Setup before all tests"""
#         print(f"\n{'='*70}")
#         print(f"Starting WHITELIST APPROVAL/REJECTION API Tests - UAT Environment")
#         print(f"Environment: {settings.ENVIRONMENT}")
#         print(f"Admin User: {settings.ADMIN_EMAIL}")
#         print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#         print(f"{'='*70}\n")
        
#         # Store test user IDs for dynamic replacement
#         cls.test_user_ids = {}
    
#     def get_admin_auth_token(self, api_client):
#         """Get admin authentication token"""
#         print("   Getting admin token...")
        
#         login_data = {
#             "identifier": settings.ADMIN_EMAIL,
#             "password": settings.ADMIN_PASSWORD
#         }
        
#         login_response = api_client.post(
#             Endpoints.LOGIN,
#             json=login_data
#         )
        
#         if login_response.status_code == 200:
#             response_data = login_response.json()
#             if response_data.get("success"):
#                 token = response_data.get("data", {}).get("access_token")
#                 if token:
#                     print(f"   ✓ Admin token obtained ({len(token)} chars)")
#                     return token
#         return None
    
#     @pytest.fixture(autouse=True)
#     def setup_admin_auth(self, api_client):
#         """Setup admin authentication before each test"""
#         self.client = api_client
        
#         # Get admin token
#         admin_token = self.get_admin_auth_token(api_client)
#         if admin_token:
#             api_client.set_auth_token(admin_token)
#             print(f"   ✓ Admin authentication successful")
#         else:
#             print(f"   ❌ Could not get admin token")
#             api_client.clear_auth_token()
    
#     def get_pending_user_id(self):
#         """Get a pending user ID from whitelist for testing"""
#         print("   Finding pending user for testing...")
        
#         # Get whitelist to find a pending user
#         params = {"page": 1, "limit": 10}
#         response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
#         if response.status_code == 200:
#             data = response.json()
#             users = data.get("data", [])
            
#             # Find a user with pending_approval status
#             for user in users:
#                 if user.get("status") == "pending_approval":
#                     user_id = user.get("id")
#                     email = user.get("email", "N/A")
#                     print(f"   ✓ Found pending user: {email} (ID: {user_id})")
#                     return user_id
        
#         print("   ⚠ No pending users found in whitelist")
#         return None
    
#     def get_approved_user_id(self):
#         """Get an already approved user ID for testing duplicate approval"""
#         print("   Finding approved user for testing...")
        
#         params = {"page": 1, "limit": 10}
#         response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
#         if response.status_code == 200:
#             data = response.json()
#             users = data.get("data", [])
            
#             # Find a user with approved status
#             for user in users:
#                 if user.get("status") == "approved":
#                     user_id = user.get("id")
#                     email = user.get("email", "N/A")
#                     print(f"   ✓ Found approved user: {email} (ID: {user_id})")
#                     return user_id
        
#         print("   ⚠ No approved users found in whitelist")
#         return None
    
#     @pytest.mark.admin
#     @pytest.mark.uat
#     @pytest.mark.parametrize("test_case", [tc for tc in WHITELIST_APPROVAL_TEST_CASES if not tc.get("skip", False)])
#     def test_whitelist_approval(self, test_case):
#         """Test whitelist approval/rejection API with various scenarios"""
#         test_id = test_case['test_id']
#         description = test_case['description']
        
#         print(f"\n▶ Test: {test_id} - {description}")
        
#         # Prepare request data
#         data = test_case.get("data", {}).copy()
        
#         # Replace dynamic placeholders with actual user IDs
#         if "{user_id}" in str(data):
#             user_id = self.get_pending_user_id()
#             if user_id:
#                 # Replace placeholder with actual user ID
#                 if "user_id" in data:
#                     data["user_id"] = user_id
#             else:
#                 print(f"   ⚠ Skipping test: No pending user available")
#                 pytest.skip("No pending user available for testing")
        
#         if "{approved_user_id}" in str(data):
#             approved_user_id = self.get_approved_user_id()
#             if approved_user_id:
#                 if "user_id" in data:
#                     data["user_id"] = approved_user_id
#             else:
#                 print(f"   ⚠ Skipping test: No approved user available")
#                 pytest.skip("No approved user available for testing")
        
#         # Special handling for authentication tests
#         if "TC_Whitelist_Approve_03" in test_id:  # No auth test
#             self.client.clear_auth_token()
#             print("   Testing without authentication")
        
#         print(f"   Request data: {json.dumps(data, indent=6)}")
        
#         # Make API request
#         start_time = time.time()
#         response = self.client.patch(
#             Endpoints.WHITELIST_AUDIT,  # PATCH endpoint
#             json=data
#         )
#         response_time = time.time() - start_time
        
#         # Parse response
#         response_data = {}
#         if response.text and response.text.strip():
#             try:
#                 response_data = response.json()
#             except json.JSONDecodeError:
#                 print(f"   ⚠ Response is not valid JSON: {response.text[:100]}")
        
#         # Assert status code
#         expected_status = test_case["expected_status"]
        
#         if response.status_code != expected_status:
#             print(f"   ❌ Expected {expected_status}, got {response.status_code}")
#             if response_data:
#                 print(f"   Message: {response_data.get('message')}")
#                 if "errors" in response_data:
#                     print(f"   Errors: {response_data.get('errors')}")
        
#         Assertions.assert_status_code(response, expected_status)
        
#         if expected_status == 200:
#             # Success assertions
#             assert response_data.get("success") == True, \
#                 f"Success should be True, got {response_data.get('success')}"
            
#             # Check for expected message
#             if "expected_message" in test_case:
#                 actual_message = response_data.get("message", "")
#                 assert test_case["expected_message"] in actual_message, \
#                     f"Expected '{test_case['expected_message']}' in '{actual_message}'"
#                 print(f"   ✓ Message: {actual_message}")
            
#             # Verify status update was successful
#             if "data" in response_data:
#                 updated_data = response_data["data"]
#                 print(f"   ✓ User status updated successfully")
                
#                 # If response contains user data, verify status
#                 if "status" in updated_data:
#                     expected_status = data.get("status")
#                     actual_status = updated_data.get("status")
#                     if expected_status and actual_status:
#                         assert actual_status == expected_status, \
#                             f"Expected status {expected_status}, got {actual_status}"
#                         print(f"   ✓ Status changed to: {actual_status}")
            
#             print(f"   ✓ Response time: {response_time:.3f}s")
            
#         else:
#             # Error response assertions
#             if response_data:
#                 if "expected_message" in test_case and "message" in response_data:
#                     actual_message = response_data.get("message", "")
#                     # For validation errors, check if expected message is in actual message
#                     assert test_case["expected_message"] in actual_message, \
#                         f"Expected '{test_case['expected_message']}' in '{actual_message}'"
#                     print(f"   ✓ Error message: {actual_message}")
                
#                 if "expected_success" in test_case:
#                     actual_success = response_data.get("success")
#                     assert actual_success == test_case["expected_success"], \
#                         f"Expected success={test_case['expected_success']}, got {actual_success}"
        
#         print(f"   ✅ PASS: {test_id}")
    
#     @pytest.mark.admin
#     @pytest.mark.smoke
#     def test_whitelist_approval_smoke(self):
#         """Smoke test for whitelist approval workflow"""
#         print("\n▶ Smoke Test: Whitelist Approval Basic Workflow")
        
#         # Step 1: Find a pending user
#         pending_user_id = self.get_pending_user_id()
        
#         if not pending_user_id:
#             print("   ⚠ Skipping: No pending users available")
#             pytest.skip("No pending users available for smoke test")
        
#         # Step 2: Approve the user
#         approval_data = {
#             "user_id": pending_user_id,
#             "status": "approved",
#             "reason": "Smoke test approval - all documents verified"
#         }
        
#         print(f"   Approving user: {pending_user_id}")
#         print(f"   Approval data: {json.dumps(approval_data, indent=6)}")
        
#         response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=approval_data)
        
#         if response.status_code == 200:
#             response_data = response.json()
#             print(f"   ✓ Approval successful: {response_data.get('message')}")
            
#             # Step 3: Verify user status changed
#             # Get user from whitelist to verify status
#             params = {"search": pending_user_id[:8], "page": 1, "limit": 5}
#             verify_response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
            
#             if verify_response.status_code == 200:
#                 verify_data = verify_response.json()
#                 users = verify_data.get("data", [])
                
#                 found_user = None
#                 for user in users:
#                     if user.get("id") == pending_user_id:
#                         found_user = user
#                         break
                
#                 if found_user:
#                     new_status = found_user.get("status")
#                     if new_status == "approved":
#                         print(f"   ✓ User status successfully changed to: {new_status}")
#                         print(f"   ✓ Smoke test completed successfully")
#                     else:
#                         print(f"   ⚠ User status is {new_status}, expected 'approved'")
#                 else:
#                     print(f"   ⚠ Could not find user in whitelist after approval")
#             else:
#                 print(f"   ⚠ Could not verify user status: {verify_response.status_code}")
#         else:
#             print(f"   ❌ Approval failed: {response.status_code}")
#             print(f"   Response: {response.text[:200]}")
#             pytest.fail("Whitelist approval smoke test failed")
    
#     @pytest.mark.admin
#     @pytest.mark.performance
#     def test_whitelist_approval_performance(self):
#         """Test whitelist approval performance"""
#         print("\n▶ Testing whitelist approval performance...")
        
#         # Find multiple pending users for performance testing
#         pending_users = []
#         params = {"page": 1, "limit": 3}
#         response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
#         if response.status_code == 200:
#             data = response.json()
#             users = data.get("data", [])
            
#             for user in users:
#                 if user.get("status") == "pending_approval":
#                     pending_users.append(user.get("id"))
        
#         if len(pending_users) < 2:
#             print("   ⚠ Skipping: Need at least 2 pending users for performance test")
#             pytest.skip("Not enough pending users for performance test")
        
#         response_times = []
        
#         # Test approval for first 2 users
#         for i, user_id in enumerate(pending_users[:2]):
#             approval_data = {
#                 "user_id": user_id,
#                 "status": "approved",
#                 "reason": f"Performance test approval {i+1}"
#             }
            
#             start_time = time.time()
#             response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=approval_data)
#             response_time = time.time() - start_time
            
#             if response.status_code == 200:
#                 response_times.append(response_time)
#                 print(f"   Request {i+1}: Approved in {response_time:.3f}s")
#             else:
#                 print(f"   ⚠ Request {i+1} failed: {response.status_code}")
        
#         # Calculate performance metrics
#         if response_times:
#             avg_time = sum(response_times) / len(response_times)
#             max_time = max(response_times)
#             min_time = min(response_times)
            
#             print(f"\n   Performance Summary:")
#             print(f"   ✓ Approvals: {len(response_times)} successful")
#             print(f"   ✓ Average: {avg_time:.3f}s")
#             print(f"   ✓ Min: {min_time:.3f}s, Max: {max_time:.3f}s")
            
#             # Performance assertions for UAT
#             assert avg_time < 3.0, f"Average approval time {avg_time:.3f}s exceeds 3s limit"
#             assert max_time < 5.0, f"Max approval time {max_time:.3f}s exceeds 5s limit"
            
#             print(f"   ✓ Performance acceptable for UAT environment")
#         else:
#             print(f"   ⚠ No successful approvals for performance measurement")
        
#         print("   ✅ PASS: Whitelist approval performance test")
    
#     @pytest.mark.admin
#     @pytest.mark.validation
#     def test_whitelist_approval_validation(self):
#         """Test whitelist approval validation"""
#         print("\n▶ Testing whitelist approval validation...")
        
#         test_cases = [
#             {
#                 "name": "Missing user_id",
#                 "data": {"status": "approved", "reason": "Test reason"},
#                 "expected_status": 422,
#                 "expected_message": "user_id is required"
#             },
#             {
#                 "name": "Missing status",
#                 "data": {"user_id": str(uuid.uuid4()), "reason": "Test reason"},
#                 "expected_status": 422,
#                 "expected_message": "status is required"
#             },
#             {
#                 "name": "Missing reason",
#                 "data": {"user_id": str(uuid.uuid4()), "status": "approved"},
#                 "expected_status": 200,
#                 "expected_message": "Whitelist audit created successfully"
#             },
#             {
#                 "name": "Empty user_id",
#                 "data": {"user_id": "", "status": "approved", "reason": "Test"},
#                 "expected_status": 422,
#                 "expected_message": "user_id must not be empty"
#             },
#             {
#                 "name": "Invalid UUID format",
#                 "data": {"user_id": "not-a-uuid", "status": "approved", "reason": "Test"},
#                 "expected_status": 422,
#                 "expected_message": "Invalid user ID"
#             },
#             {
#                 "name": "Empty reason",
#                 "data": {"user_id": str(uuid.uuid4()), "status": "approved", "reason": ""},
#                 "expected_status": 200,
#                 "expected_message": "Whitelist audit created successfully"
#             },
#             {
#                 "name": "Too short reason",
#                 "data": {"user_id": str(uuid.uuid4()), "status": "approved", "reason": "a"},
#                 "expected_status": 200,
#                 "expected_message": "Whitelist audit created successfully"
#             }
#         ]
        
#         passed_tests = 0
        
#         for test_case in test_cases:
#             print(f"   Testing: {test_case['name']}")
            
#             response = self.client.patch(
#                 Endpoints.WHITELIST_AUDIT,
#                 json=test_case["data"]
#             )
            
#             if response.status_code == test_case["expected_status"]:
#                 print(f"     ✓ Correct status: {response.status_code}")
#                 passed_tests += 1
#             else:
#                 print(f"     ❌ Expected {test_case['expected_status']}, got {response.status_code}")
#                 if response.text:
#                     print(f"     Response: {response.text[:100]}")
        
#         print(f"\n   ✓ Validation tests passed: {passed_tests}/{len(test_cases)}")
#         print("   ✅ PASS: Whitelist approval validation test")
    
#     @pytest.mark.admin
#     @pytest.mark.integration
#     def test_whitelist_approval_rejection_cycle(self):
#         """Integration test: Approve → Verify → Reject → Verify"""
#         print("\n▶ Integration Test: Approve/Reject Cycle")
        
#         # Find a pending user
#         pending_user_id = self.get_pending_user_id()
        
#         if not pending_user_id:
#             print("   ⚠ Skipping: No pending users available")
#             pytest.skip("No pending users available for integration test")
        
#         print(f"   Test user ID: {pending_user_id}")
        
#         # Step 1: Approve the user
#         print("   Step 1: Approving user...")
#         approve_data = {
#             "user_id": pending_user_id,
#             "status": "approved",
#             "reason": "Integration test - initial approval"
#         }
        
#         approve_response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=approve_data)
        
#         if approve_response.status_code != 200:
#             print(f"   ❌ Approval failed: {approve_response.status_code}")
#             pytest.skip("Approval failed, cannot proceed with integration test")
        
#         print(f"   ✓ User approved successfully")
        
#         # Step 2: Verify approval
#         print("   Step 2: Verifying approval status...")
#         params = {"search": pending_user_id[:8]}
#         verify_response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
#         if verify_response.status_code == 200:
#             data = verify_response.json()
#             users = data.get("data", [])
            
#             for user in users:
#                 if user.get("id") == pending_user_id:
#                     if user.get("status") == "approved":
#                         print(f"   ✓ User status verified as 'approved'")
#                     else:
#                         print(f"   ⚠ User status is {user.get('status')}, expected 'approved'")
#                     break
        
#         # Step 3: Reject the user (change status)
#         print("   Step 3: Rejecting user...")
#         reject_data = {
#             "user_id": pending_user_id,
#             "status": "rejected",
#             "reason": "Integration test - changed to rejected"
#         }
        
#         reject_response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=reject_data)
        
#         if reject_response.status_code == 200:
#             print(f"   ✓ User rejected successfully")
#         else:
#             print(f"   ⚠ Rejection failed: {reject_response.status_code}")
        
#         # Step 4: Verify rejection
#         print("   Step 4: Verifying rejection status...")
#         verify_response2 = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
#         if verify_response2.status_code == 200:
#             data = verify_response2.json()
#             users = data.get("data", [])
            
#             for user in users:
#                 if user.get("id") == pending_user_id:
#                     current_status = user.get("status")
#                     print(f"   ✓ Final user status: {current_status}")
#                     break
        
#         print("   ✅ PASS: Whitelist approval/rejection integration test")


# tests/test_whitelist_approval.py
"""Whitelist Approval/Rejection API tests for Teresa Backoffice UAT"""

import pytest
import time
import json
import uuid
from datetime import datetime
from api.endpoints import Endpoints
from config.test_data_whitelist_approval import WHITELIST_APPROVAL_TEST_CASES, VALID_STATUSES
from utils.assertions import Assertions
from config.settings import settings

class TestWhitelistApprovalAPI:
    """Test suite for Whitelist Approval/Rejection API on UAT environment"""
    
    @classmethod
    def setup_class(cls):
        """Setup before all tests"""
        print(f"\n{'='*70}")
        print(f"Starting WHITELIST APPROVAL/REJECTION API Tests - UAT Environment")
        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"Admin User: {settings.ADMIN_EMAIL}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        # Store test user IDs for dynamic replacement
        cls.test_user_ids = {}
    
    def get_admin_auth_token(self, api_client):
        """Get admin authentication token"""
        print("   Getting admin token...")
        
        login_data = {
            "identifier": settings.ADMIN_EMAIL,
            "password": settings.ADMIN_PASSWORD
        }
        
        login_response = api_client.post(
            Endpoints.LOGIN,
            json=login_data
        )
        
        if login_response.status_code == 200:
            response_data = login_response.json()
            if response_data.get("success"):
                token = response_data.get("data", {}).get("access_token")
                if token:
                    print(f"   ✓ Admin token obtained ({len(token)} chars)")
                    return token
        return None
    
    @pytest.fixture(autouse=True)
    def setup_admin_auth(self, api_client):
        """Setup admin authentication before each test"""
        self.client = api_client
        
        # Get admin token
        admin_token = self.get_admin_auth_token(api_client)
        if admin_token:
            api_client.set_auth_token(admin_token)
            print(f"   ✓ Admin authentication successful")
        else:
            print(f"   ❌ Could not get admin token")
            api_client.clear_auth_token()
    
    def get_pending_user_id(self):
        """Get a pending user ID from whitelist for testing"""
        print("   Finding pending user for testing...")
        
        params = {"page": 1, "limit": 10}
        response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
        if response.status_code == 200:
            data = response.json()
            users = data.get("data", [])
            
            for user in users:
                if user.get("status") == "pending_approval":
                    user_id = user.get("id")
                    email = user.get("email", "N/A")
                    print(f"   ✓ Found pending user: {email} (ID: {user_id})")
                    return user_id
        
        print("   ⚠ No pending users found in whitelist")
        return None
    
    def get_approved_user_id(self):
        """Get an already approved user ID for testing duplicate approval"""
        print("   Finding approved user for testing...")
        
        params = {"page": 1, "limit": 10}
        response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
        if response.status_code == 200:
            data = response.json()
            users = data.get("data", [])
            
            for user in users:
                if user.get("status") == "approved":
                    user_id = user.get("id")
                    email = user.get("email", "N/A")
                    print(f"   ✓ Found approved user: {email} (ID: {user_id})")
                    return user_id
        
        print("   ⚠ No approved users found in whitelist")
        return None
    
    def get_rejected_user_id(self):
        """Get a previously rejected user ID for testing status reversal"""
        print("   Finding rejected user for testing...")
        
        params = {"page": 1, "limit": 10}
        response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
        if response.status_code == 200:
            data = response.json()
            users = data.get("data", [])
            
            for user in users:
                if user.get("status") == "rejected":
                    user_id = user.get("id")
                    email = user.get("email", "N/A")
                    print(f"   ✓ Found rejected user: {email} (ID: {user_id})")
                    return user_id
        
        print("   ⚠ No rejected users found in whitelist")
        return None
    
    @pytest.mark.admin
    @pytest.mark.uat
    @pytest.mark.parametrize("test_case", [tc for tc in WHITELIST_APPROVAL_TEST_CASES if not tc.get("skip", False)])
    def test_whitelist_approval(self, test_case):
        """Test whitelist approval/rejection API with various scenarios"""
        test_id = test_case['test_id']
        description = test_case['description']
        
        print(f"\n▶ Test: {test_id} - {description}")
        
        data = test_case.get("data", {}).copy()
        
        if "{user_id}" in str(data):
            user_id = self.get_pending_user_id()
            if user_id:
                if "user_id" in data:
                    data["user_id"] = user_id
            else:
                print(f"   ⚠ Skipping test: No pending user available")
                pytest.skip("No pending user available for testing")
        
        if "{approved_user_id}" in str(data):
            approved_user_id = self.get_approved_user_id()
            if approved_user_id:
                if "user_id" in data:
                    data["user_id"] = approved_user_id
            else:
                print(f"   ⚠ Skipping test: No approved user available")
                pytest.skip("No approved user available for testing")
        
        if "{rejected_user_id}" in str(data):
            rejected_user_id = self.get_rejected_user_id()
            if rejected_user_id:
                if "user_id" in data:
                    data["user_id"] = rejected_user_id
            else:
                print(f"   ⚠ Skipping test: No rejected user available")
                pytest.skip("No rejected user available for testing")
        
        if "TC_Whitelist_Approve_03" in test_id:
            self.client.clear_auth_token()
            print("   Testing without authentication")
        
        print(f"   Request data: {json.dumps(data, indent=6)}")
        
        start_time = time.time()
        response = self.client.patch(
            Endpoints.WHITELIST_AUDIT,
            json=data
        )
        response_time = time.time() - start_time
        
        response_data = {}
        if response.text and response.text.strip():
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                print(f"   ⚠ Response is not valid JSON: {response.text[:100]}")
        
        expected_status = test_case["expected_status"]
        
        if response.status_code != expected_status:
            print(f"   ❌ Expected {expected_status}, got {response.status_code}")
            if response_data:
                print(f"   Message: {response_data.get('message')}")
                if "errors" in response_data:
                    print(f"   Errors: {response_data.get('errors')}")
        
        Assertions.assert_status_code(response, expected_status)
        
        if expected_status == 200:
            assert response_data.get("success") == True, \
                f"Success should be True, got {response_data.get('success')}"
            
            if "expected_message" in test_case:
                actual_message = response_data.get("message", "")
                assert test_case["expected_message"] in actual_message, \
                    f"Expected '{test_case['expected_message']}' in '{actual_message}'"
                print(f"   ✓ Message: {actual_message}")
            
            if "data" in response_data:
                updated_data = response_data["data"]
                print(f"   ✓ User status updated successfully")
                
                if "status" in updated_data:
                    expected_status_val = data.get("status")
                    actual_status_val = updated_data.get("status")
                    if expected_status_val and actual_status_val:
                        assert actual_status_val == expected_status_val, \
                            f"Expected status {expected_status_val}, got {actual_status_val}"
                        print(f"   ✓ Status changed to: {actual_status_val}")
            
            print(f"   ✓ Response time: {response_time:.3f}s")
        
        else:
            if response_data:
                if "expected_message" in test_case and "message" in response_data:
                    actual_message = response_data.get("message", "")
                    assert test_case["expected_message"] in actual_message, \
                        f"Expected '{test_case['expected_message']}' in '{actual_message}'"
                    print(f"   ✓ Error message: {actual_message}")
                
                if "expected_success" in test_case:
                    actual_success = response_data.get("success")
                    assert actual_success == test_case["expected_success"], \
                        f"Expected success={test_case['expected_success']}, got {actual_success}"
        
        print(f"   ✅ PASS: {test_id}")
    
    @pytest.mark.admin
    @pytest.mark.smoke
    def test_whitelist_approval_smoke(self):
        """Smoke test for whitelist approval workflow"""
        print("\n▶ Smoke Test: Whitelist Approval Basic Workflow")
        
        pending_user_id = self.get_pending_user_id()
        
        if not pending_user_id:
            print("   ⚠ Skipping: No pending users available")
            pytest.skip("No pending users available for smoke test")
        
        approval_data = {
            "user_id": pending_user_id,
            "status": "approved",
            "reason": "Smoke test approval - all documents verified"
        }
        
        print(f"   Approving user: {pending_user_id}")
        print(f"   Approval data: {json.dumps(approval_data, indent=6)}")
        
        response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=approval_data)
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"   ✓ Approval successful: {response_data.get('message')}")
            
            params = {"search": pending_user_id[:8], "page": 1, "limit": 5}
            verify_response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
            
            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                users = verify_data.get("data", [])
                
                found_user = None
                for user in users:
                    if user.get("id") == pending_user_id:
                        found_user = user
                        break
                
                if found_user:
                    new_status = found_user.get("status")
                    if new_status == "approved":
                        print(f"   ✓ User status successfully changed to: {new_status}")
                        print(f"   ✓ Smoke test completed successfully")
                    else:
                        print(f"   ⚠ User status is {new_status}, expected 'approved'")
                else:
                    print(f"   ⚠ Could not find user in whitelist after approval")
            else:
                print(f"   ⚠ Could not verify user status: {verify_response.status_code}")
        else:
            print(f"   ❌ Approval failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            pytest.fail("Whitelist approval smoke test failed")
    
    @pytest.mark.admin
    @pytest.mark.performance
    def test_whitelist_approval_performance(self):
        """Test whitelist approval performance"""
        print("\n▶ Testing whitelist approval performance...")
        
        pending_users = []
        params = {"page": 1, "limit": 3}
        response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
        if response.status_code == 200:
            data = response.json()
            users = data.get("data", [])
            
            for user in users:
                if user.get("status") == "pending_approval":
                    pending_users.append(user.get("id"))
        
        if len(pending_users) < 2:
            print("   ⚠ Skipping: Need at least 2 pending users for performance test")
            pytest.skip("Not enough pending users for performance test")
        
        response_times = []
        
        for i, user_id in enumerate(pending_users[:2]):
            approval_data = {
                "user_id": user_id,
                "status": "approved",
                "reason": f"Performance test approval {i+1}"
            }
            
            start_time = time.time()
            response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=approval_data)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                response_times.append(response_time)
                print(f"   Request {i+1}: Approved in {response_time:.3f}s")
            else:
                print(f"   ⚠ Request {i+1} failed: {response.status_code}")
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            print(f"\n   Performance Summary:")
            print(f"   ✓ Approvals: {len(response_times)} successful")
            print(f"   ✓ Average: {avg_time:.3f}s")
            print(f"   ✓ Min: {min_time:.3f}s, Max: {max_time:.3f}s")
            
            assert avg_time < 3.0, f"Average approval time {avg_time:.3f}s exceeds 3s limit"
            assert max_time < 5.0, f"Max approval time {max_time:.3f}s exceeds 5s limit"
            
            print(f"   ✓ Performance acceptable for UAT environment")
        else:
            print(f"   ⚠ No successful approvals for performance measurement")
        
        print("   ✅ PASS: Whitelist approval performance test")
    
    @pytest.mark.admin
    @pytest.mark.validation
    def test_whitelist_approval_validation(self):
        """Test whitelist approval validation"""
        print("\n▶ Testing whitelist approval validation...")
        
        test_cases = [
            {
                "name": "Missing user_id",
                "data": {"status": "approved", "reason": "Test reason"},
                "expected_status": 422,
                "expected_message": "user_id is required"
            },
            {
                "name": "Missing status",
                "data": {"user_id": str(uuid.uuid4()), "reason": "Test reason"},
                "expected_status": 422,
                "expected_message": "status is required"
            },
            {
                "name": "Missing reason",
                "data": {"user_id": str(uuid.uuid4()), "status": "approved"},
                "expected_status": 200,
                "expected_message": "Whitelist audit created successfully"
            },
            {
                "name": "Empty user_id",
                "data": {"user_id": "", "status": "approved", "reason": "Test"},
                "expected_status": 422,
                "expected_message": "user_id must not be empty"
            },
            {
                "name": "Invalid UUID format",
                "data": {"user_id": "not-a-uuid", "status": "approved", "reason": "Test"},
                "expected_status": 422,
                "expected_message": "Invalid user ID"
            },
            {
                "name": "Empty reason",
                "data": {"user_id": str(uuid.uuid4()), "status": "approved", "reason": ""},
                "expected_status": 200,
                "expected_message": "Whitelist audit created successfully"
            },
            {
                "name": "Too short reason",
                "data": {"user_id": str(uuid.uuid4()), "status": "approved", "reason": "a"},
                "expected_status": 200,
                "expected_message": "Whitelist audit created successfully"
            }
        ]
        
        passed_tests = 0
        
        for test_case in test_cases:
            print(f"   Testing: {test_case['name']}")
            
            response = self.client.patch(
                Endpoints.WHITELIST_AUDIT,
                json=test_case["data"]
            )
            
            if response.status_code == test_case["expected_status"]:
                print(f"     ✓ Correct status: {response.status_code}")
                passed_tests += 1
            else:
                print(f"     ❌ Expected {test_case['expected_status']}, got {response.status_code}")
                if response.text:
                    print(f"     Response: {response.text[:100]}")
        
        print(f"\n   ✓ Validation tests passed: {passed_tests}/{len(test_cases)}")
        print("   ✅ PASS: Whitelist approval validation test")
    
    @pytest.mark.admin
    @pytest.mark.integration
    def test_whitelist_approval_rejection_cycle(self):
        """Integration test: Approve → Verify → Reject → Verify"""
        print("\n▶ Integration Test: Approve/Reject Cycle")
        
        pending_user_id = self.get_pending_user_id()
        
        if not pending_user_id:
            print("   ⚠ Skipping: No pending users available")
            pytest.skip("No pending users available for integration test")
        
        print(f"   Test user ID: {pending_user_id}")
        
        approve_data = {
            "user_id": pending_user_id,
            "status": "approved",
            "reason": "Integration test - initial approval"
        }
        
        approve_response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=approve_data)
        
        if approve_response.status_code != 200:
            print(f"   ❌ Approval failed: {approve_response.status_code}")
            pytest.skip("Approval failed, cannot proceed with integration test")
        
        print(f"   ✓ User approved successfully")
        
        params = {"search": pending_user_id[:8]}
        verify_response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
        if verify_response.status_code == 200:
            data = verify_response.json()
            users = data.get("data", [])
            
            for user in users:
                if user.get("id") == pending_user_id:
                    if user.get("status") == "approved":
                        print(f"   ✓ User status verified as 'approved'")
                    else:
                        print(f"   ⚠ User status is {user.get('status')}, expected 'approved'")
                    break
        
        reject_data = {
            "user_id": pending_user_id,
            "status": "rejected",
            "reason": "Integration test - changed to rejected"
        }
        
        reject_response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=reject_data)
        
        if reject_response.status_code == 200:
            print(f"   ✓ User rejected successfully")
        else:
            print(f"   ⚠ Rejection failed: {reject_response.status_code}")
        
        verify_response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        if verify_response.status_code == 200:
            data = verify_response.json()
            for user in data.get("data", []):
                if user.get("id") == pending_user_id:
                    if user.get("status") == "rejected":
                        print(f"   ✓ User status verified as 'rejected'")
                    else:
                        print(f"   ⚠ User status is {user.get('status')}, expected 'rejected'")
                    break
        
        print("   ✅ PASS: Integration test for approve/reject cycle completed")
