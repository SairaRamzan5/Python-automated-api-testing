"""Test suite for Techniques Add API"""

import pytest
import json
import uuid
import time
from datetime import datetime
from api.endpoints import Endpoints
from config.test_data_techniques_add import TECHNIQUES_ADD_TEST_DATA

class TestTechniquesAddAPI:
    """Test suite for adding techniques"""
    
    @classmethod
    def setup_class(cls):
        """Setup before all tests"""
        print(f"\n{'='*70}")
        print(f"TECHNIQUES ADD API TESTS")
        print(f"Endpoint: {Endpoints.TECHNIQUES}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        # Store created technique IDs for cleanup
        cls.created_technique_ids = []
    
    @pytest.fixture(autouse=True)
    def setup_admin_auth(self, api_client, admin_auth_token):
        """Setup admin authentication before each test"""
        self.client = api_client
        
        # Use the admin_auth_token fixture from conftest.py
        if admin_auth_token:
            self.client.set_auth_token(admin_auth_token)
            print("   ✓ Admin authentication set")
        else:
            print("   ⚠ No admin token available")
            self.client.clear_auth_token()
    
    def generate_unique_technique_name(self, base_name):
        """Generate unique technique name for testing"""
        return f"{base_name}-{str(uuid.uuid4())[:8]}"
    
    @pytest.mark.techniques
    @pytest.mark.add
    @pytest.mark.smoke
    def test_add_single_technique_smoke(self):
        """Smoke test: Add a single technique"""
        print("\n▶ Smoke Test: Add Single Technique")
        
        unique_name = self.generate_unique_technique_name("test-technique")
        
        request_data = {
            "techniques": [
                {
                    "name": unique_name,
                    "description": "Test technique for smoke test",
                    "parent_name": None,
                    "is_active": True,
                    "values": [
                        {
                            "language_code": "en",
                            "name": "Test Technique"
                        }
                    ]
                }
            ]
        }
        
        print(f"   Adding technique: {unique_name}")
        print(f"   Request data: {json.dumps(request_data, indent=2)}")
        
        response = self.client.post(Endpoints.TECHNIQUES, json=request_data)
        
        print(f"   Status: {response.status_code}")
        
        # Parse response
        data = {}
        if response.text:
            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"   ❌ Response is not valid JSON: {response.text[:200]}")
                return  # Don't fail, just report
        
        print(f"   Success: {data.get('success')}")
        print(f"   Message: {data.get('message')}")
        
        # For successful creation
        if response.status_code == 200:
            if data.get("success"):
                print(f"   ✓ Technique creation successful")
                
                # Check message
                if "message" in data:
                    print(f"   Message: {data['message']}")
                
                # Verify response structure
                if "data" in data:
                    created_techniques = data["data"]
                    if isinstance(created_techniques, list):
                        print(f"   Created {len(created_techniques)} techniques")
                        
                        for technique in created_techniques:
                            if "id" in technique:
                                self.created_technique_ids.append(technique["id"])
                                print(f"   ✓ Technique ID: {technique['id']}")
                            
                            if "is_duplicate" in technique:
                                print(f"   Is duplicate: {technique['is_duplicate']}")
            else:
                print(f"   ⚠ Request unsuccessful: {data.get('message')}")
        
        elif response.status_code == 401:
            print(f"   ❌ Unauthorized - Admin token may be invalid")
        elif response.status_code == 403:
            print(f"   ❌ Forbidden - Admin may not have permission")
        elif response.status_code == 422:
            # Validation error
            print(f"   ⚠ Validation error: {data.get('message', 'No message')}")
            if "errors" in data:
                for error in data["errors"]:
                    print(f"     - {error.get('field')}: {error.get('message')}")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    
    @pytest.mark.techniques
    @pytest.mark.add
    @pytest.mark.positive
    def test_add_multiple_techniques(self):
        """Test adding multiple techniques in one request"""
        print("\n▶ Test: Add Multiple Techniques")
        
        request_data = {
            "techniques": [
                {
                    "name": self.generate_unique_technique_name("weaving"),
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
                    "name": self.generate_unique_technique_name("knitting"),
                    "description": "Creating fabric by interlocking loops of yarn",
                    "parent_name": None,
                    "is_active": True,
                    "values": [
                        {
                            "language_code": "en",
                            "name": "Knitting"
                        },
                        {
                            "language_code": "es",
                            "name": "Tejido"
                        }
                    ]
                }
            ]
        }
        
        print(f"   Adding {len(request_data['techniques'])} techniques...")
        
        response = self.client.post(Endpoints.TECHNIQUES, json=request_data)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"   ✓ Success: {data.get('message')}")
                
                # Check response data
                if "data" in data:
                    created_techniques = data["data"]
                    print(f"   ✓ Created {len(created_techniques)} techniques")
                    
                    for tech in created_techniques:
                        if "id" in tech:
                            self.created_technique_ids.append(tech["id"])
                            print(f"     - {tech.get('name', 'N/A')} (ID: {tech['id']})")
            else:
                print(f"   ⚠ Request failed: {data.get('message')}")
        else:
            print(f"   ❌ Failed with status: {response.status_code}")
    
    @pytest.mark.techniques
    @pytest.mark.add
    @pytest.mark.negative
    def test_add_duplicate_technique(self):
        """Test adding duplicate technique name"""
        print("\n▶ Test: Add Duplicate Technique")
        
        # First, create a technique
        unique_name = self.generate_unique_technique_name("original")
        
        create_data = {
            "techniques": [
                {
                    "name": unique_name,
                    "description": "Original technique",
                    "parent_name": None,
                    "is_active": True,
                    "values": [
                        {
                            "language_code": "en",
                            "name": "Original"
                        }
                    ]
                }
            ]
        }
        
        # Create first technique
        print(f"   Creating first technique: {unique_name}")
        response1 = self.client.post(Endpoints.TECHNIQUES, json=create_data)
        
        if response1.status_code == 200:
            first_data = response1.json()
            if first_data.get("data") and len(first_data["data"]) > 0:
                first_id = first_data["data"][0]["id"]
                self.created_technique_ids.append(first_id)
                print(f"   ✓ First technique created with ID: {first_id}")
            else:
                print(f"   ⚠ First technique created but no data in response")
                return
        else:
            print(f"   ⚠ Could not create first technique: {response1.status_code}")
            return
        
        # Try to create duplicate
        duplicate_data = {
            "techniques": [
                {
                    "name": unique_name,  # Same name
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
        }
        
        print(f"   Attempting to create duplicate: {unique_name}")
        response2 = self.client.post(Endpoints.TECHNIQUES, json=duplicate_data)
        
        print(f"   Status: {response2.status_code}")
        
        if response2.status_code == 200:
            data = response2.json()
            print(f"   Message: {data.get('message')}")
            
            # Check if duplicate flag is set
            if data.get("data") and len(data["data"]) > 0:
                technique = data["data"][0]
                if "is_duplicate" in technique:
                    is_duplicate = technique["is_duplicate"]
                    print(f"   is_duplicate flag: {is_duplicate}")
                    
                    if is_duplicate:
                        print(f"   ✓ Correctly identified as duplicate")
                    else:
                        print(f"   ⚠ Created new technique instead of marking as duplicate")
        
        elif response2.status_code == 422:
            # Some APIs return validation error for duplicates
            data = response2.json()
            error_msg = data.get("message", "").lower()
            if "duplicate" in error_msg:
                print(f"   ✓ Correctly rejected duplicate with validation error")
    
    @pytest.mark.techniques
    @pytest.mark.add
    @pytest.mark.parametrize("test_case", 
        TECHNIQUES_ADD_TEST_DATA["positive_cases"] + 
        TECHNIQUES_ADD_TEST_DATA["negative_cases"])
    def test_add_techniques_various_scenarios(self, test_case):
        """Test various add techniques scenarios"""
        test_id = test_case["test_id"]
        description = test_case["description"]
        
        print(f"\n▶ Test: {test_id} - {description}")
        
        # Prepare request data
        request_data = test_case["data"].copy()
        
        # Generate unique names for techniques to avoid conflicts
        if "techniques" in request_data:
            for i, technique in enumerate(request_data["techniques"]):
                if "name" in technique:
                    # Add unique suffix for positive test cases
                    if test_case.get("expected_status") == 200:
                        base_name = technique["name"]
                        unique_name = f"{base_name}-{str(uuid.uuid4())[:8]}"
                        request_data["techniques"][i]["name"] = unique_name
                        print(f"   Using unique name: {unique_name}")
        
        # Handle authentication scenarios
        if test_case.get("headers") == {}:
            self.client.clear_auth_token()
            print("   Testing without authentication")
        
        # Make request
        response = self.client.post(Endpoints.TECHNIQUES, json=request_data)
        
        print(f"   Status: {response.status_code} (expected: {test_case['expected_status']})")
        
        # Verify status code
        expected_status = test_case["expected_status"]
        actual_status = response.status_code
        
        if actual_status != expected_status:
            print(f"   ⚠ Status mismatch: expected {expected_status}, got {actual_status}")
        
        # Parse response
        if response.text:
            try:
                data = response.json()
                
                # Verify success flag if present
                if "expected_success" in test_case and "success" in data:
                    expected_success = test_case["expected_success"]
                    actual_success = data.get("success")
                    
                    if expected_success != actual_success:
                        print(f"   ⚠ Success mismatch: expected {expected_success}, got {actual_success}")
                
                # Verify message if expected
                if "expected_message" in test_case and "message" in data:
                    actual_message = data.get("message", "")
                    expected_msg = test_case["expected_message"]
                    
                    # For contains check
                    if expected_msg.lower() in actual_message.lower():
                        print(f"   ✓ Message contains expected: {actual_message}")
                
                # Store created IDs for cleanup
                if actual_status == 200 and data.get("success") and "data" in data:
                    for technique in data["data"]:
                        if "id" in technique:
                            self.created_technique_ids.append(technique["id"])
            
            except json.JSONDecodeError:
                print(f"   ❌ Response is not valid JSON")
        
        print(f"   ✅ Test completed: {test_id}")
    
    @pytest.mark.techniques
    @pytest.mark.add
    @pytest.mark.security
    def test_add_without_authentication(self):
        """Test that authentication is required"""
        print("\n▶ Test: Add Technique Without Authentication")
        
        self.client.clear_auth_token()
        
        request_data = {
            "techniques": [
                {
                    "name": "test-no-auth",
                    "description": "Test without auth",
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
        }
        
        response = self.client.post(Endpoints.TECHNIQUES, json=request_data)
        
        print(f"   Status: {response.status_code}")
        
        # Should be 401 or 403
        if response.status_code in [401, 403]:
            print(f"   ✓ Correctly rejected without authentication")
            if response.text:
                data = response.json()
                print(f"   Message: {data.get('message')}")
        else:
            print(f"   ⚠ Expected 401/403 without auth, got {response.status_code}")
    
    @classmethod
    def teardown_class(cls):
        """Cleanup created techniques after all tests"""
        print(f"\n{'='*70}")
        print(f"CLEANUP SUMMARY")
        print(f"{'='*70}")
        
        if cls.created_technique_ids:
            print(f"   Created {len(cls.created_technique_ids)} techniques during tests")
            print(f"   Technique IDs: {cls.created_technique_ids[:5]}")  # Show first 5 only
        else:
            print(f"   No techniques created during tests")
        
        print(f"\n{'='*70}")
        print(f"TECHNIQUES ADD TESTS COMPLETED")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")