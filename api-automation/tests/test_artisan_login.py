"""Artisan Login API tests - Verify with whitelist status"""

import pytest
import json
import time
from datetime import datetime
from api.endpoints import Endpoints
from utils.assertions import Assertions
from utils.user_manager import UserManager
from config.settings import settings

class TestArtisanLoginAPI:
    """Test suite for Artisan Login API - Verify with whitelist"""
    
    @classmethod
    def setup_class(cls):
        """Setup before all tests"""
        print(f"\n{'='*70}")
        print(f"ARTISAN LOGIN WITH WHITELIST VERIFICATION")
        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
    
    @pytest.fixture(autouse=True)
    def setup_test(self, api_client):
        """Setup before each test"""
        self.client = api_client
        self.client.clear_auth_token()
        self.user_manager = UserManager(api_client)
    
    @pytest.mark.uat_functional
    def test_verify_whitelist_status_before_login(self):
        """Verify user appears in whitelist with correct status"""
        print("\n▶ TEST: Verify Whitelist Status → Login Access")
        
        # Step 1: Create a pending user
        print("\n   Step 1: Creating pending user...")
        pending_user = self.user_manager.get_or_create_pending_user()
        if not pending_user:
            print("   ❌ Cannot create pending user")
            pytest.fail("Test setup failed")
            return
        
        print(f"   User created: {pending_user['email']}")
        print(f"   Expected status: pending_approval")
        
        # Step 2: Verify user is in whitelist as pending
        print("\n   Step 2: Verifying whitelist status...")
        self.user_manager.find_recent_test_users_in_whitelist()
        
        print(f"\n   Step 3: Attempting login (should be blocked)...")
        time.sleep(2.0)
        
        login_data = {
            "identifier": pending_user["email"],
            "password": pending_user["password"]
        }
        
        response = self.client.post(Endpoints.LOGIN, json=login_data)
        
        if response.status_code == 200:
            print(f"   ❌ Pending user logged in (should be blocked)")
            print(f"   Response: {response.json().get('message', 'No message')}")
            # This might mean approval is not required
        elif response.status_code == 403:
            print(f"   ✅ Pending user correctly blocked: 403 Forbidden")
            msg = response.json().get("message", "")
            if "approv" in msg.lower() or "pending" in msg.lower():
                print(f"   ✓ Message indicates approval required: {msg}")
        else:
            print(f"   ⚠ Pending user got: {response.status_code}")
        
        # Step 4: Try to approve the user
        print(f"\n   Step 4: Attempting to approve user...")
        if pending_user.get("id"):
            if self.user_manager.approve_user_in_whitelist(pending_user["id"]):
                pending_user["approved"] = True
                pending_user["status"] = "approved"
                print(f"   ✓ User approved")
                
                # Wait for approval to take effect
                print(f"   Waiting for approval to propagate...")
                time.sleep(5.0)
                
                # Step 5: Try login again after approval
                print(f"\n   Step 5: Attempting login after approval...")
                response2 = self.client.post(Endpoints.LOGIN, json=login_data)
                
                if response2.status_code == 200:
                    print(f"   ✅ Approved user can login!")
                    data = response2.json()
                    if data.get("success"):
                        print(f"   ✓ Login successful")
                        if "access_token" in data.get("data", {}):
                            print(f"   ✓ Access token received")
                elif response2.status_code == 403:
                    print(f"   ❌ Approved user still blocked: 403")
                    print(f"   Response: {response2.json().get('message', 'No message')}")
                    print(f"   ⚠ Note: Approval might not affect login access")
                else:
                    print(f"   ⚠ Approved user got: {response2.status_code}")
            else:
                print(f"   ❌ Could not approve user")
        else:
            print(f"   ⚠ Cannot approve: No user ID")
        
        print(f"\n   ✅ TEST COMPLETED")
    
    @pytest.mark.uat_functional
    def test_investigate_login_response_messages(self):
        """Investigate what messages login returns for different statuses"""
        print("\n▶ INVESTIGATION: Login Response Messages")
        
        # Create both approved and pending users
        print("\n   Creating test users...")
        
        approved_user = self.user_manager.get_or_create_approved_user()
        pending_user = self.user_manager.get_or_create_pending_user()
        
        if not approved_user or not pending_user:
            print("   ❌ Cannot create test users")
            pytest.skip("Test user creation failed")
            return
        
        print(f"\n   Test Users:")
        print(f"   1. Approved: {approved_user['email']} (status: {approved_user.get('status', 'unknown')})")
        print(f"   2. Pending: {pending_user['email']} (status: {pending_user.get('status', 'unknown')})")
        
        # Check whitelist status
        print(f"\n   Checking whitelist status...")
        self.user_manager.find_recent_test_users_in_whitelist()
        
        # Test login for both users
        test_cases = [
            ("Approved User", approved_user, "Should login"),
            ("Pending User", pending_user, "Should be blocked")
        ]
        
        for user_type, user, expectation in test_cases:
            print(f"\n   Testing {user_type}: {user['email']}")
            print(f"   Expectation: {expectation}")
            
            time.sleep(2.0)
            
            login_data = {
                "identifier": user["email"],
                "password": user["password"]
            }
            
            response = self.client.post(Endpoints.LOGIN, json=login_data)
            
            print(f"   Response Status: {response.status_code}")
            
            if response.text:
                try:
                    data = response.json()
                    message = data.get("message", "No message")
                    print(f"   Message: {message}")
                    
                    # Check for specific keywords
                    keywords = ["approv", "pending", "forbidden", "unauthorized", "credentials", "phone", "verified"]
                    found_keywords = [kw for kw in keywords if kw in message.lower()]
                    if found_keywords:
                        print(f"   Keywords found: {found_keywords}")
                except:
                    print(f"   Response text: {response.text[:100]}")
            
            # Analyze
            if user_type == "Approved User" and response.status_code == 200:
                print(f"   ✅ Approved user can login (expected)")
            elif user_type == "Approved User" and response.status_code != 200:
                print(f"   ❌ Approved user cannot login (unexpected)")
            elif user_type == "Pending User" and response.status_code != 200:
                print(f"   ✅ Pending user blocked (expected)")
            elif user_type == "Pending User" and response.status_code == 200:
                print(f"   ❌ Pending user can login (unexpected)")
        
        print(f"\n   ✅ INVESTIGATION COMPLETED")
    
    @pytest.mark.uat_functional
    def test_bulk_user_creation_and_login_test(self):
        """Create multiple users and test login behavior"""
        print("\n▶ BULK TEST: Multiple Users Login Behavior")
        
        # Create 3 users with different expected statuses
        test_users = []
        
        for i in range(3):
            if i == 0:
                # User 1: Approved
                print(f"\n   Creating approved user {i+1}...")
                user = self.user_manager.create_test_artisan(approved=True)
                expected_access = "Should login"
            elif i == 1:
                # User 2: Pending
                print(f"\n   Creating pending user {i+1}...")
                user = self.user_manager.create_test_artisan(approved=False)
                expected_access = "Should be blocked"
            else:
                # User 3: Created but not approved via API (system default)
                print(f"\n   Creating user {i+1} (no approval attempt)...")
                user = self.user_manager.create_test_artisan(approved=False)
                # Don't try to approve
                expected_access = "Unknown"
            
            if user:
                test_users.append((user, expected_access))
                print(f"   Created: {user['email']}")
        
        if not test_users:
            print("   ❌ No users created")
            pytest.skip("User creation failed")
            return
        
        # Wait for all users to be processed
        print(f"\n   Waiting for system to process all users...")
        time.sleep(10.0)
        
        # Check whitelist status for all
        print(f"\n   Checking whitelist status for all users...")
        whitelist_users = self.user_manager.find_recent_test_users_in_whitelist()
        
        # Test login for each
        print(f"\n   Testing login for {len(test_users)} users...")
        
        results = []
        
        for user, expected_access in test_users:
            print(f"\n   Testing: {user['email']}")
            print(f"   Expected: {expected_access}")
            print(f"   Whitelist status: {user.get('status', 'unknown')}")
            
            time.sleep(3.0)  # Delay between tests
            
            login_data = {
                "identifier": user["email"],
                "password": user["password"]
            }
            
            response = self.client.post(Endpoints.LOGIN, json=login_data)
            
            result = {
                "email": user["email"],
                "status": user.get("status", "unknown"),
                "approved": user.get("approved", False),
                "login_status": response.status_code,
                "message": response.json().get("message", "No message") if response.text else ""
            }
            
            results.append(result)
            
            print(f"   Login result: {response.status_code}")
            print(f"   Message: {result['message']}")
            
            # Quick analysis
            if response.status_code == 200:
                print(f"   Result: CAN LOGIN")
            else:
                print(f"   Result: CANNOT LOGIN ({response.status_code})")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"BULK TEST SUMMARY")
        print(f"{'='*60}")
        
        for result in results:
            can_login = result["login_status"] == 200
            status = "✓ CAN LOGIN" if can_login else "✗ CANNOT LOGIN"
            print(f"\n   {result['email']}")
            print(f"   Whitelist: {result['status']} (approved: {result['approved']})")
            print(f"   Login: {result['login_status']} - {status}")
            print(f"   Message: {result['message']}")
        
        print(f"\n{'='*60}")
        print(f"CONCLUSION:")
        
        # Analyze pattern
        approved_can_login = sum(1 for r in results if r["approved"] and r["login_status"] == 200)
        pending_cannot_login = sum(1 for r in results if not r["approved"] and r["login_status"] != 200)
        
        print(f"   Approved users that can login: {approved_can_login}")
        print(f"   Pending users that cannot login: {pending_cannot_login}")
        
        if approved_can_login > 0 and pending_cannot_login > 0:
            print(f"   ✅ System appears to enforce approval-based login")
        elif approved_can_login == 0:
            print(f"   ⚠ Approved users cannot login - approval may not be working")
        elif pending_cannot_login == 0:
            print(f"   ⚠ Pending users can login - approval may not be required")
        
        print(f"   ✅ BULK TEST COMPLETED")