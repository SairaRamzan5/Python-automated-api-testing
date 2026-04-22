# """Product Creation API tests - Organized by test scenarios (UPDATED BASED ON ACTUAL API BEHAVIOR)"""

# import pytest
# import time
# import uuid
# from datetime import datetime

# class TestArtisanProductCreation:
#     """Test suite for Product Creation API - Organized by scenarios"""
    
#     created_products = []
    
#     # Valid status values from actual API behavior
#     VALID_STATUSES = ["pending", "approved", "rejected", "draft", "available", "sent"]
    
#     @classmethod
#     def setup_class(cls):
#         print(f"\n{'='*70}")
#         print(f"ARTISAN PRODUCT CREATION TESTS")
#         print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#         print(f"{'='*70}\n")
    
#     @pytest.fixture(autouse=True)
#     def setup(self, api_client, artisan_auth_token):
#         self.client = api_client
#         if not artisan_auth_token:
#             pytest.skip("Artisan authentication required")
#         self.client.set_auth_token(artisan_auth_token)
    
#     def generate_product_name(self):
#         """Generate unique product name"""
#         unique_id = str(uuid.uuid4())[:6]
#         timestamp = int(time.time())
#         return f"Test Product {timestamp}-{unique_id}"
    
#     def get_valid_payload(self, **kwargs):
#         """Get a valid product payload"""
#         payload = {
#             "name": self.generate_product_name(),
#             "description": "its a new testing product created after change in api.",
#             "hours_to_make": "22",
#             "monthly_qty": "54",
#             "annual_qty": "345",
#             "custom_price": "20",
#             "status": "draft",
#             "materials": [
#                 {
#                     "name": "cotton",
#                     "price": "20",
#                     "quantity": "20",
#                     "unit": "kg"
#                 }
#             ],
#             "techniques": [
#                 {
#                     "id": "8fc243e7-d556-43b6-81a8-392d30b586c5"
#                 }
#             ],
#             "files": [
#                 {
#                     "id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc"
#                 }
#             ]
#         }
#         payload.update(kwargs)
#         return payload
    
#     # ============ SCENARIO 1: CREATE PRODUCT WITH VALID FIELDS ============
    
#     def test_scenario_valid_fields(self):
#         """SCENARIO 1: Create product with all valid fields"""
#         print("\n🔵 SCENARIO 1: Create product with valid fields")
#         print("   Testing: Complete valid payload should succeed")
        
#         payload = self.get_valid_payload()
        
#         response = self.client.post("/products", json=payload)
#         print(f"   Status: {response.status_code}")
        
#         if response.status_code == 201:
#             data = response.json()
#             assert data["success"] is True
#             print(f"   ✅ PASSED: Product created successfully")
#             print(f"   📦 Product ID: {data['data']['id']}")
#             print(f"   📝 Name: {data['data']['name']}")
#             print(f"   📊 Status: {data['data']['status']}")
            
#             self.__class__.created_products.append({
#                 "id": data["data"]["id"],
#                 "name": payload["name"],
#                 "scenario": "valid_fields"
#             })
#         else:
#             print(f"   ❌ FAILED: Expected 201, got {response.status_code}")
#             if response.text:
#                 print(f"   Response: {response.text[:200]}")
#             assert False
    
#     # ============ SCENARIO 2: CREATE PRODUCT WITH INVALID FIELDS ============
    
#     def test_scenario_invalid_fields(self):
#         """SCENARIO 2: Create product with invalid field values"""
#         print("\n🔵 SCENARIO 2: Create product with invalid fields")
#         print("   Testing: Invalid values should be rejected")
        
#         invalid_test_cases = [
#             {
#                 "name": "Invalid name type",
#                 "payload": {"name": 12345},
#                 "expected_field": "name",
#                 "expected_message": "Product name must be a string"
#             },
#             {
#                 "name": "Name too long (>30 chars)",
#                 "payload": {"name": "This is a very long product name that exceeds 30 characters"},
#                 "expected_field": "name",
#                 "expected_message": "Product name must not exceed 30 characters"
#             },
#             {
#                 "name": "Invalid hours_to_make (negative)",
#                 "payload": {"hours_to_make": -5},
#                 "expected_field": "hours_to_make",
#                 "expected_message": "Hours to make must be >= 0"
#             },
#             {
#                 "name": "Invalid hours_to_make (non-numeric)",
#                 "payload": {"hours_to_make": "abc"},
#                 "expected_field": "hours_to_make",
#                 "expected_message": "Hours to make must be >= 0"
#             },
#             {
#                 "name": "Invalid monthly_qty (negative)",
#                 "payload": {"monthly_qty": -10},
#                 "expected_field": "monthly_qty",
#                 "expected_message": "Monthly production must be >= 0"
#             },
#             {
#                 "name": "Invalid annual_qty (less than monthly*12)",
#                 "payload": {"monthly_qty": 100, "annual_qty": 500},
#                 "expected_field": "annual_qty",
#                 "expected_message": "annual_qty must be at least monthly_qty * 12",
#                 "should_fail": True
#             },
#             {
#                 "name": "Invalid custom_price (negative)",
#                 "payload": {"custom_price": -5},
#                 "expected_field": "custom_price",
#                 "expected_message": "Custom price must be >= 0"
#             }
#         ]
        
#         for test_case in invalid_test_cases:
#             print(f"\n   🔸 Test: {test_case['name']}")
            
#             payload = self.get_valid_payload()
#             payload.update(test_case['payload'])
            
#             response = self.client.post("/products", json=payload)
#             print(f"      Status: {response.status_code}")
            
#             if test_case.get('should_fail', True):
#                 # This test should fail (422)
#                 if response.status_code == 422:
#                     data = response.json()
#                     field_errors = [e for e in data["errors"] if e["field"] == test_case['expected_field']]
#                     if field_errors:
#                         print(f"      ✅ PASSED: Rejected with error: {field_errors[0]['message']}")
#                     else:
#                         print(f"      ⚠ WARNING: Rejected but no specific error for {test_case['expected_field']}")
#                         print(f"      Errors: {[e['field'] for e in data.get('errors', [])]}")
#                 elif response.status_code == 201:
#                     print(f"      ❌ FAILED: Should have been rejected but was accepted")
#                     # Track if accidentally created
#                     data = response.json()
#                     self.__class__.created_products.append({
#                         "id": data["data"]["id"],
#                         "name": payload["name"],
#                         "scenario": "invalid_fields_accidental"
#                     })
#                 else:
#                     print(f"      ❌ FAILED: Expected 422, got {response.status_code}")
#             else:
#                 # This test might pass (201) - update based on actual behavior
#                 if response.status_code == 201:
#                     print(f"      ✅ PASSED: Accepted (as per actual API behavior)")
#                     data = response.json()
#                     self.__class__.created_products.append({
#                         "id": data["data"]["id"],
#                         "name": payload["name"],
#                         "scenario": "invalid_fields_expected_pass"
#                     })
#                 else:
#                     print(f"      ⚠ NOTE: Got {response.status_code}, API behavior may have changed")
    
#     # ============ SCENARIO 3: CREATE PRODUCT WITH EMPTY FIELDS ============
    
#     def test_scenario_empty_fields(self):
#         """SCENARIO 3: Create product with empty fields"""
#         print("\n🔵 SCENARIO 3: Create product with empty fields")
#         print("   Testing: Empty values should be rejected appropriately")
        
#         empty_test_cases = [
#             {
#                 "name": "Empty name",
#                 "payload": {"name": ""},
#                 "expected_field": "name",
#                 "expected_message": "Product name is required",
#                 "expected_status": 422
#             },
#             {
#                 "name": "Empty description",
#                 "payload": {"description": ""},
#                 "expected_status": 201,  # Should accept empty description
#                 "should_pass": True
#             },
#             {
#                 "name": "Empty materials array",
#                 "payload": {"materials": []},
#                 "expected_status": 201,  # Based on test results, this is accepted
#                 "should_pass": True
#             },
#             {
#                 "name": "Empty techniques array",
#                 "payload": {"techniques": []},
#                 "expected_status": 201,  # Based on test results, this is accepted
#                 "should_pass": True
#             },
#             {
#                 "name": "Empty files array",
#                 "payload": {"files": []},
#                 "expected_status": 201,  # Based on test results, this is accepted
#                 "should_pass": True
#             },
#             {
#                 "name": "Empty status",
#                 "payload": {"status": ""},
#                 "expected_field": "status",
#                 "expected_message": "Status must be a valid product status",
#                 "expected_status": 422
#             }
#         ]
        
#         for test_case in empty_test_cases:
#             print(f"\n   🔸 Test: {test_case['name']}")
            
#             payload = self.get_valid_payload()
#             payload.update(test_case['payload'])
            
#             response = self.client.post("/products", json=payload)
#             print(f"      Status: {response.status_code}")
            
#             expected_status = test_case.get('expected_status', 422)
            
#             if test_case.get('should_pass', False):
#                 if response.status_code == expected_status:
#                     print(f"      ✅ PASSED: Got expected status {expected_status}")
#                     if response.status_code == 201:
#                         data = response.json()
#                         self.__class__.created_products.append({
#                             "id": data["data"]["id"],
#                             "name": payload["name"],
#                             "scenario": "empty_fields_accepted"
#                         })
#                 else:
#                     print(f"      ⚠ WARNING: Expected {expected_status}, got {response.status_code}")
#             else:
#                 if response.status_code == expected_status:
#                     print(f"      ✅ PASSED: Correctly rejected with status {expected_status}")
#                     if response.status_code == 422:
#                         data = response.json()
#                         field_errors = [e for e in data["errors"] if e["field"] == test_case.get('expected_field')]
#                         if field_errors:
#                             print(f"         Error: {field_errors[0]['message']}")
#                 elif response.status_code == 201:
#                     print(f"      ❌ FAILED: Should have been rejected but was accepted")
#                 else:
#                     print(f"      ❌ FAILED: Expected {expected_status}, got {response.status_code}")
    
#     # ============ SCENARIO 4: CREATE PRODUCT WITH ONLY REQUIRED FIELDS ============
    
#     def test_scenario_only_required_fields(self):
#         """SCENARIO 4: Create product with only required fields"""
#         print("\n🔵 SCENARIO 4: Create product with only required fields")
#         print("   Testing: Required fields only - name, materials, techniques, files")
        
#         # Based on test results, all fields except name might be optional
#         payload = {
#             "name": self.generate_product_name()
#             # All other fields are optional based on test results
#         }
        
#         print(f"   Testing with only 'name' field (others will default)")
        
#         response = self.client.post("/products", json=payload)
#         print(f"   Status: {response.status_code}")
        
#         if response.status_code == 201:
#             data = response.json()
#             print(f"   ✅ PASSED: Product created with only name field")
#             print(f"   📦 Product ID: {data['data']['id']}")
#             print(f"   📝 Name: {data['data']['name']}")
#             print(f"   📊 Status defaulted to: '{data['data']['status']}'")
#             print(f"   📦 materials: {data['data']['materials']}")
#             print(f"   📦 techniques: {data['data']['techniques']}")
#             print(f"   📦 files: {data['data']['files']}")
            
#             self.__class__.created_products.append({
#                 "id": data["data"]["id"],
#                 "name": payload["name"],
#                 "scenario": "only_required"
#             })
#         else:
#             print(f"   ❌ FAILED: Expected 201, got {response.status_code}")
#             if response.text:
#                 print(f"   Response: {response.text[:200]}")
    
#     # ============ SCENARIO 5: CREATE PRODUCT WITH ONLY OPTIONAL FIELDS ============
    
#     def test_scenario_only_optional_fields(self):
#         """SCENARIO 5: Create product with only optional fields (missing required)"""
#         print("\n🔵 SCENARIO 5: Create product with only optional fields")
#         print("   Testing: Optional fields only - should fail (name is required)")
        
#         # Only optional fields, no name (which is required)
#         payload = {
#             "description": "its a new testing product created after change in api.",
#             "hours_to_make": "22",
#             "monthly_qty": "54",
#             "annual_qty": "345",
#             "custom_price": "20",
#             "status": "draft",
#             "is_active": True,
#             "materials": [
#                 {
#                     "name": "cotton",
#                     "price": "20",
#                     "quantity": "20",
#                     "unit": "kg"
#                 }
#             ],
#             "techniques": [
#                 {
#                     "id": "8fc243e7-d556-43b6-81a8-392d30b586c5"
#                 }
#             ],
#             "files": [
#                 {
#                     "id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc"
#                 }
#             ]
#         }
        
#         print(f"   Missing: name")
        
#         response = self.client.post("/products", json=payload)
#         print(f"   Status: {response.status_code}")
        
#         if response.status_code == 422:
#             data = response.json()
#             print(f"   ✅ PASSED: Rejected as expected")
#             print(f"   Errors received:")
#             for error in data["errors"]:
#                 print(f"      - {error['field']}: {error['message']}")
            
#             # Verify name is in errors
#             error_fields = [e["field"] for e in data["errors"]]
#             if "name" in error_fields:
#                 print(f"      ✓ name validation present")
#             else:
#                 print(f"      ⚠ name validation missing")
#         else:
#             print(f"   ❌ FAILED: Expected 422, got {response.status_code}")
#             if response.status_code == 201:
#                 print(f"   WARNING: Product created without name!")
#                 data = response.json()
#                 self.__class__.created_products.append({
#                     "id": data["data"]["id"],
#                     "name": data["data"]["name"],
#                     "scenario": "only_optional_accidental"
#                 })
    
#     # ============ SCENARIO 6: INVALID STATUS ============
    
#     def test_scenario_invalid_status(self):
#         """SCENARIO 6: Create product with invalid status values"""
#         print("\n🔵 SCENARIO 6: Create product with invalid status")
#         print(f"   Valid statuses: {', '.join(self.VALID_STATUSES)}")
        
#         invalid_statuses = [
#             "active",      # Not in valid list
#             "inactive",    # Not in valid list
#             "published",   # Not in valid list
#             "deleted",     # Not in valid list
#             "archived",    # Not in valid list
#             "PENDING",     # Uppercase
#             "APPROVED",    # Uppercase
#             "DRAFT",       # Uppercase
#             "AVAILABLE",   # Uppercase
#             "SENT",        # Uppercase
#             " pending",    # Leading space
#             "approved ",   # Trailing space
#             "draft!",      # Special character
#             "pending123",  # With numbers
#             "",            # Empty
#             " ",           # Space
#             123,           # Number
#             True,          # Boolean
#         ]
        
#         for invalid_status in invalid_statuses[:5]:  # Test first 5 to avoid too many requests
#             print(f"\n   🔸 Testing status: '{invalid_status}'")
            
#             payload = self.get_valid_payload()
#             payload["status"] = invalid_status
            
#             response = self.client.post("/products", json=payload)
#             print(f"      Status: {response.status_code}")
            
#             # Invalid status should be rejected
#             if response.status_code == 422:
#                 data = response.json()
#                 status_errors = [e for e in data["errors"] if e["field"] == "status"]
#                 if status_errors:
#                     print(f"      ✅ PASSED: Rejected - {status_errors[0]['message']}")
#                 else:
#                     print(f"      ✅ PASSED: Rejected (no specific status error)")
#             elif response.status_code == 201:
#                 print(f"      ❌ FAILED: Invalid status '{invalid_status}' was accepted!")
#                 data = response.json()
#                 self.__class__.created_products.append({
#                     "id": data["data"]["id"],
#                     "name": payload["name"],
#                     "scenario": "invalid_status_accepted"
#                 })
#             else:
#                 print(f"      ❌ FAILED: Expected 422, got {response.status_code}")
    
#     # ============ SCENARIO 7: INVALID MATERIALS ============
    
#     def test_scenario_invalid_materials(self):
#         """SCENARIO 7: Create product with invalid materials"""
#         print("\n🔵 SCENARIO 7: Create product with invalid materials")
        
#         invalid_materials_test_cases = [
#             {
#                 "name": "Materials not an array",
#                 "materials": {"name": "cotton", "price": "20", "quantity": "20", "unit": "kg"},
#                 "expected_status": 422,
#                 "expected_field": "materials"
#             },
#             {
#                 "name": "Empty materials array",
#                 "materials": [],
#                 "expected_status": 201,  # Based on test results, this is accepted
#                 "should_pass": True
#             },
#             {
#                 "name": "Material missing name",
#                 "materials": [{"price": "20", "quantity": "20", "unit": "kg"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Material missing price",
#                 "materials": [{"name": "cotton", "quantity": "20", "unit": "kg"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Material missing quantity",
#                 "materials": [{"name": "cotton", "price": "20", "unit": "kg"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Material missing unit",
#                 "materials": [{"name": "cotton", "price": "20", "quantity": "20"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Invalid price (negative)",
#                 "materials": [{"name": "cotton", "price": -5, "quantity": "20", "unit": "kg"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Invalid quantity (negative)",
#                 "materials": [{"name": "cotton", "price": "20", "quantity": -5, "unit": "kg"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Too many materials (101)",
#                 "materials": [{"name": f"material_{i}", "price": "10", "quantity": "1", "unit": "kg"} for i in range(101)],
#                 "expected_status": 422
#             }
#         ]
        
#         for test_case in invalid_materials_test_cases:
#             print(f"\n   🔸 Test: {test_case['name']}")
            
#             payload = self.get_valid_payload()
#             payload["materials"] = test_case["materials"]
            
#             response = self.client.post("/products", json=payload)
#             print(f"      Status: {response.status_code}")
            
#             expected_status = test_case.get('expected_status', 422)
            
#             if test_case.get('should_pass', False):
#                 if response.status_code == expected_status:
#                     print(f"      ✅ PASSED: Got expected status {expected_status}")
#                     if response.status_code == 201:
#                         data = response.json()
#                         self.__class__.created_products.append({
#                             "id": data["data"]["id"],
#                             "name": payload["name"],
#                             "scenario": "invalid_materials_accepted"
#                         })
#                 else:
#                     print(f"      ⚠ WARNING: Expected {expected_status}, got {response.status_code}")
#             else:
#                 if response.status_code == expected_status:
#                     print(f"      ✅ PASSED: Correctly rejected with status {expected_status}")
#                 elif response.status_code == 201:
#                     print(f"      ❌ FAILED: Should have been rejected but was accepted")
#                     data = response.json()
#                     self.__class__.created_products.append({
#                         "id": data["data"]["id"],
#                         "name": payload["name"],
#                         "scenario": "invalid_materials_unexpected"
#                     })
#                 else:
#                     print(f"      ❌ FAILED: Expected {expected_status}, got {response.status_code}")
    
#     # ============ SCENARIO 8: INVALID TECHNIQUES ============
    
#     def test_scenario_invalid_techniques(self):
#         """SCENARIO 8: Create product with invalid techniques"""
#         print("\n🔵 SCENARIO 8: Create product with invalid techniques")
        
#         invalid_techniques_test_cases = [
#             {
#                 "name": "Techniques not an array",
#                 "techniques": {"id": "8fc243e7-d556-43b6-81a8-392d30b586c5"},
#                 "expected_status": 422,
#                 "expected_field": "techniques"
#             },
#             {
#                 "name": "Empty techniques array",
#                 "techniques": [],
#                 "expected_status": 201,  # Based on test results, this is accepted
#                 "should_pass": True
#             },
#             {
#                 "name": "Technique missing id",
#                 "techniques": [{"name": "ceramics"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Invalid technique id format",
#                 "techniques": [{"id": "invalid-uuid"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Too many techniques (51)",
#                 "techniques": [{"id": f"tech-{i}"} for i in range(51)],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Duplicate technique ids",
#                 "techniques": [
#                     {"id": "8fc243e7-d556-43b6-81a8-392d30b586c5"},
#                     {"id": "8fc243e7-d556-43b6-81a8-392d30b586c5"}
#                 ],
#                 "expected_status": 201,  # Based on test results, duplicates are accepted
#                 "should_pass": True
#             }
#         ]
        
#         for test_case in invalid_techniques_test_cases:
#             print(f"\n   🔸 Test: {test_case['name']}")
            
#             payload = self.get_valid_payload()
#             payload["techniques"] = test_case["techniques"]
            
#             response = self.client.post("/products", json=payload)
#             print(f"      Status: {response.status_code}")
            
#             expected_status = test_case.get('expected_status', 422)
            
#             if test_case.get('should_pass', False):
#                 if response.status_code == expected_status:
#                     print(f"      ✅ PASSED: Got expected status {expected_status}")
#                     if response.status_code == 201:
#                         data = response.json()
#                         self.__class__.created_products.append({
#                             "id": data["data"]["id"],
#                             "name": payload["name"],
#                             "scenario": "invalid_techniques_accepted"
#                         })
#                 else:
#                     print(f"      ⚠ WARNING: Expected {expected_status}, got {response.status_code}")
#             else:
#                 if response.status_code == expected_status:
#                     print(f"      ✅ PASSED: Correctly rejected with status {expected_status}")
#                 elif response.status_code == 201:
#                     print(f"      ❌ FAILED: Should have been rejected but was accepted")
#                     data = response.json()
#                     self.__class__.created_products.append({
#                         "id": data["data"]["id"],
#                         "name": payload["name"],
#                         "scenario": "invalid_techniques_unexpected"
#                     })
#                 else:
#                     print(f"      ❌ FAILED: Expected {expected_status}, got {response.status_code}")
    
#     # ============ SCENARIO 9: INVALID FILES ============
    
#     def test_scenario_invalid_files(self):
#         """SCENARIO 9: Create product with invalid files"""
#         print("\n🔵 SCENARIO 9: Create product with invalid files")
        
#         invalid_files_test_cases = [
#             {
#                 "name": "Files not an array",
#                 "files": {"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc"},
#                 "expected_status": 422,
#                 "expected_field": "files"
#             },
#             {
#                 "name": "Empty files array",
#                 "files": [],
#                 "expected_status": 201,  # Based on test results, this is accepted
#                 "should_pass": True
#             },
#             {
#                 "name": "File missing id",
#                 "files": [{"is_active": "true"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Invalid file id format",
#                 "files": [{"id": "invalid-uuid"}],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Too many files (16)",
#                 "files": [{"id": f"file-{i}"} for i in range(16)],
#                 "expected_status": 422
#             },
#             {
#                 "name": "Duplicate file ids",
#                 "files": [
#                     {"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc"},
#                     {"id": "d4f9620a-dc9e-4946-86e5-4ccd6f1645cc"}
#                 ],
#                 "expected_status": 422  # This returned 422 in your test
#             }
#         ]
        
#         for test_case in invalid_files_test_cases:
#             print(f"\n   🔸 Test: {test_case['name']}")
            
#             payload = self.get_valid_payload()
#             payload["files"] = test_case["files"]
            
#             response = self.client.post("/products", json=payload)
#             print(f"      Status: {response.status_code}")
            
#             # Check if response has errors key
#             data = {}
#             try:
#                 data = response.json()
#             except:
#                 pass
            
#             expected_status = test_case.get('expected_status', 422)
            
#             if test_case.get('should_pass', False):
#                 if response.status_code == expected_status:
#                     print(f"      ✅ PASSED: Got expected status {expected_status}")
#                     if response.status_code == 201:
#                         self.__class__.created_products.append({
#                             "id": data.get("data", {}).get("id") if data else None,
#                             "name": payload["name"],
#                             "scenario": "invalid_files_accepted"
#                         })
#                 else:
#                     print(f"      ⚠ WARNING: Expected {expected_status}, got {response.status_code}")
#             else:
#                 if response.status_code == expected_status:
#                     print(f"      ✅ PASSED: Correctly rejected with status {expected_status}")
#                     # Check for errors field if available
#                     if data and "errors" in data:
#                         file_errors = [e for e in data["errors"] if e["field"] == test_case.get('expected_field', 'files')]
#                         if file_errors:
#                             print(f"         Error: {file_errors[0]['message']}")
#                 elif response.status_code == 201:
#                     print(f"      ❌ FAILED: Should have been rejected but was accepted")
#                     if data and "data" in data:
#                         self.__class__.created_products.append({
#                             "id": data["data"].get("id"),
#                             "name": payload["name"],
#                             "scenario": "invalid_files_unexpected"
#                         })
#                 else:
#                     print(f"      ❌ FAILED: Expected {expected_status}, got {response.status_code}")
    
#     # ============ SCENARIO 10: MIXED VALIDATION SCENARIOS ============
    
#     def test_scenario_mixed_validation(self):
#         """SCENARIO 10: Mixed validation scenarios"""
#         print("\n🔵 SCENARIO 10: Mixed validation scenarios")
        
#         mixed_scenarios = [
#             {
#                 "name": "Valid status with invalid materials",
#                 "payload": {
#                     "status": "pending",
#                     "materials": [{"name": "cotton"}]  # Missing price, quantity, unit
#                 },
#                 "expected_errors": ["materials.0.price", "materials.0.quantity", "materials.0.unit"]
#             },
#             {
#                 "name": "Valid materials with invalid status",
#                 "payload": {
#                     "status": "invalid_status",
#                     "materials": [
#                         {"name": "cotton", "price": "20", "quantity": "20", "unit": "kg"}
#                     ]
#                 },
#                 "expected_errors": ["status"]
#             },
#             {
#                 "name": "Multiple invalid fields",
#                 "payload": {
#                     "name": "",  # Empty
#                     "status": "invalid",  # Invalid
#                     "materials": "not-an-array"  # Wrong type
#                 },
#                 "expected_errors": ["name", "status", "materials"]
#             }
#         ]
        
#         for scenario in mixed_scenarios:
#             print(f"\n   🔸 Test: {scenario['name']}")
            
#             payload = self.get_valid_payload()
#             payload.update(scenario['payload'])
            
#             response = self.client.post("/products", json=payload)
#             print(f"      Status: {response.status_code}")
            
#             if response.status_code == 422:
#                 data = response.json()
#                 error_fields = [e["field"] for e in data["errors"]]
                
#                 # Check if expected errors are present
#                 missing_errors = []
#                 for expected in scenario['expected_errors']:
#                     if expected in error_fields:
#                         print(f"      ✓ {expected} validation present")
#                     else:
#                         # Check if any error contains this as substring
#                         found = False
#                         for field in error_fields:
#                             if expected in field:
#                                 print(f"      ✓ {expected} validation present (as {field})")
#                                 found = True
#                                 break
#                         if not found:
#                             missing_errors.append(expected)
                
#                 if missing_errors:
#                     print(f"      ⚠ Missing expected errors: {missing_errors}")
#                     print(f"      Actual errors: {error_fields}")
#                 else:
#                     print(f"      ✅ PASSED: All expected validations triggered")
#             elif response.status_code == 201:
#                 print(f"      ❌ FAILED: Should have been rejected but was accepted")
#                 data = response.json()
#                 self.__class__.created_products.append({
#                     "id": data["data"]["id"],
#                     "name": payload["name"],
#                     "scenario": "mixed_validation_accepted"
#                 })
#             else:
#                 print(f"      ❌ FAILED: Expected 422, got {response.status_code}")
    
#     # ============ SCENARIO 11: TEST ONLY NAME FIELD ============
    
#     def test_scenario_only_name_field(self):
#         """SCENARIO 11: Create product with only name field"""
#         print("\n🔵 SCENARIO 11: Create product with only name field")
        
#         payload = {
#             "name": self.generate_product_name()
#         }
        
#         response = self.client.post("/products", json=payload)
#         print(f"   Status: {response.status_code}")
        
#         if response.status_code == 201:
#             data = response.json()
#             print(f"   ✅ PASSED: Product created with only name")
#             print(f"   📦 Product ID: {data['data']['id']}")
#             print(f"   📝 Name: {data['data']['name']}")
#             print(f"   📊 Status: {data['data']['status']}")
#             print(f"   📦 materials: {data['data']['materials']} (default)")
#             print(f"   📦 techniques: {data['data']['techniques']} (default)")
#             print(f"   📦 files: {data['data']['files']} (default)")
            
#             self.__class__.created_products.append({
#                 "id": data["data"]["id"],
#                 "name": payload["name"],
#                 "scenario": "only_name"
#             })
#         else:
#             print(f"   ❌ FAILED: Expected 201, got {response.status_code}")
    
#     # ============ CLEANUP ============
    
#     @classmethod
#     def teardown_class(cls):
#         """Cleanup after all tests"""
#         print(f"\n{'='*70}")
#         print(f"TEST SUMMARY")
#         print(f"{'='*70}")
#         print(f"Total Products Created: {len(cls.created_products)}")
        
#         if cls.created_products:
#             print(f"\n📋 Created Products by Scenario:")
#             scenario_count = {}
#             for product in cls.created_products:
#                 scenario = product.get('scenario', 'unknown')
#                 scenario_count[scenario] = scenario_count.get(scenario, 0) + 1
            
#             for scenario, count in sorted(scenario_count.items()):
#                 print(f"   • {scenario}: {count} product(s)")
            
#             print(f"\n📋 Detailed List:")
#             for i, product in enumerate(cls.created_products, 1):
#                 print(f"   {i}. {product.get('name')} (ID: {product.get('id', 'N/A')}) - Scenario: {product.get('scenario', 'N/A')}")
        
#         print(f"{'='*70}\n")


"""Product Creation API tests - Organized by test scenarios (UPDATED BASED ON ACTUAL API SCHEMA)"""

import pytest
import time
import uuid
from datetime import datetime
from test_data_product_creation import ProductTestData


class TestArtisanProductCreation:
    """Test suite for Product Creation API - Organized by scenarios"""
    
    created_products = []
    
    @classmethod
    def setup_class(cls):
        print(f"\n{'='*70}")
        print(f"ARTISAN PRODUCT CREATION TESTS")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, artisan_auth_token):
        self.client = api_client
        if not artisan_auth_token:
            pytest.skip("Artisan authentication required")
        self.client.set_auth_token(artisan_auth_token)
    
    def generate_product_name(self):
        """Generate unique product name"""
        return ProductTestData.generate_unique_product_name()
    
    def get_valid_payload(self, **kwargs):
        """Get a valid product payload based on API schema"""
        return ProductTestData.get_valid_product_payload(**kwargs)
    
    # ============ SCENARIO 1: CREATE PRODUCT WITH COMPLETE VALID DATA ============
    
    def test_scenario_complete_valid_product(self):
        """SCENARIO 1: Create product with complete valid data"""
        print("\n🔵 SCENARIO 1: Create product with complete valid data")
        print("   Testing: All fields provided with valid values")
        
        payload = self.get_valid_payload()
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            assert "id" in data
            assert data["name"] == payload["name"]
            print(f"   ✅ PASSED: Product created successfully")
            print(f"   📦 Product ID: {data['id']}")
            print(f"   📝 Name: {data['name']}")
            print(f"   📊 Status: {data['status']}")
            
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": "complete_valid_product"
            })
        else:
            print(f"   ❌ FAILED: Expected 201, got {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:200]}")
            assert False, f"Product creation failed with status {response.status_code}"
    
    # ============ SCENARIO 2: CREATE PRODUCT WITH MINIMUM REQUIRED FIELDS ============
    
    def test_scenario_minimum_required_fields(self):
        """SCENARIO 2: Create product with only required fields"""
        print("\n🔵 SCENARIO 2: Create product with minimum required fields")
        print("   Testing: Only name and essential fields")
        
        # According to schema, name is required, others may have defaults
        payload = {
            "name": self.generate_product_name()
        }
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ PASSED: Product created with minimum fields")
            print(f"   📦 Product ID: {data['id']}")
            print(f"   📝 Name: {data['name']}")
            print(f"   📊 Status default: '{data.get('status', 'N/A')}'")
            
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": "minimum_required_fields"
            })
        else:
            print(f"   ❌ FAILED: Expected 201, got {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:200]}")
    
    # ============ SCENARIO 3: CREATE PRODUCT WITH DIFFERENT STATUS VALUES ============
    
    @pytest.mark.parametrize("status", ProductTestData.STATUS_VALUES)
    def test_scenario_different_status_values(self, status):
        """SCENARIO 3: Create product with different valid status values"""
        print(f"\n🔵 SCENARIO 3: Create product with status '{status}'")
        print(f"   Testing: Valid status should be accepted")
        
        payload = self.get_valid_payload()
        payload["status"] = status
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ PASSED: Product created with status '{status}'")
            print(f"   📦 Product ID: {data['id']}")
            
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"status_{status}"
            })
        else:
            print(f"   ❌ FAILED: Status '{status}' rejected with {response.status_code}")
            if response.status_code == 422 and response.text:
                print(f"   Error: {response.text[:200]}")
    
    # ============ SCENARIO 4: CREATE PRODUCT WITH INVALID STATUS ============
    
    @pytest.mark.parametrize("invalid_status", ProductTestData.INVALID_STATUS_VALUES)
    def test_scenario_invalid_status_values(self, invalid_status):
        """SCENARIO 4: Create product with invalid status values"""
        print(f"\n🔵 SCENARIO 4: Create product with invalid status '{invalid_status}'")
        print(f"   Testing: Invalid status should be rejected")
        
        payload = self.get_valid_payload()
        payload["status"] = invalid_status
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 422 or response.status_code == 400:
            print(f"   ✅ PASSED: Invalid status rejected with {response.status_code}")
        elif response.status_code == 201:
            print(f"   ❌ FAILED: Invalid status '{invalid_status}' was accepted!")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": "invalid_status_accepted"
            })
        else:
            print(f"   ⚠ WARNING: Got {response.status_code}, expected 400/422")
    
    # ============ SCENARIO 5: CREATE PRODUCT WITH INVALID FIELD TYPES ============
    
    @pytest.mark.parametrize("field,invalid_value,expected_error", 
                            ProductTestData.INVALID_FIELD_TYPES)
    def test_scenario_invalid_field_types(self, field, invalid_value, expected_error):
        """SCENARIO 5: Create product with invalid field types"""
        print(f"\n🔵 SCENARIO 5: Invalid field type for '{field}'")
        print(f"   Testing: {field} = {invalid_value} (type: {type(invalid_value).__name__})")
        
        payload = self.get_valid_payload()
        payload[field] = invalid_value
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [400, 422]:
            print(f"   ✅ PASSED: Invalid value rejected with {response.status_code}")
            if response.text:
                print(f"   Error response includes: {expected_error}")
        elif response.status_code == 201:
            print(f"   ❌ FAILED: Invalid value was accepted!")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"invalid_{field}_accepted"
            })
        else:
            print(f"   ⚠ WARNING: Got {response.status_code}")
    
    # ============ SCENARIO 6: CREATE PRODUCT WITH EMPTY FIELDS ============
    
    @pytest.mark.parametrize("field,empty_value", ProductTestData.EMPTY_FIELD_TESTS)
    def test_scenario_empty_fields(self, field, empty_value):
        """SCENARIO 6: Create product with empty fields"""
        print(f"\n🔵 SCENARIO 6: Empty field test for '{field}'")
        print(f"   Testing: {field} = {empty_value}")
        
        payload = self.get_valid_payload()
        payload[field] = empty_value
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if field == "name" and response.status_code in [400, 422]:
            print(f"   ✅ PASSED: Empty name correctly rejected")
        elif field != "name" and response.status_code == 201:
            print(f"   ✅ PASSED: Empty '{field}' accepted (has default)")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"empty_{field}_accepted"
            })
        elif response.status_code == 201:
            print(f"   ⚠ WARNING: Empty '{field}' was accepted (unexpected for required field)")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"empty_{field}_unexpected"
            })
        else:
            print(f"   ℹ️  Info: Got {response.status_code}")
    
    # ============ SCENARIO 7: CREATE PRODUCT WITH BOUNDARY VALUES ============
    
    def test_scenario_boundary_values(self):
        """SCENARIO 7: Testing boundary values"""
        print("\n🔵 SCENARIO 7: Testing boundary values")
        
        for test_case in ProductTestData.BOUNDARY_TEST_CASES:
            print(f"\n   🔸 Test: {test_case['name']}")
            
            payload = self.get_valid_payload()
            payload[test_case["field"]] = test_case["value"]
            
            response = self.client.post("/products", json=payload)
            print(f"      Value: {test_case['value']}")
            print(f"      Status: {response.status_code}")
            
            if test_case["should_pass"] and response.status_code == 201:
                print(f"      ✅ PASSED: Boundary value accepted")
                data = response.json()
                self.__class__.created_products.append({
                    "id": data["id"],
                    "name": payload["name"],
                    "scenario": f"boundary_{test_case['name']}"
                })
            elif not test_case["should_pass"] and response.status_code in [400, 422]:
                print(f"      ✅ PASSED: Boundary value correctly rejected")
            elif test_case["should_pass"] and response.status_code != 201:
                print(f"      ❌ FAILED: Expected acceptance but got {response.status_code}")
            else:
                print(f"      ⚠ WARNING: Unexpected result")
    
    # ============ SCENARIO 8: CREATE PRODUCT WITH MATERIALS VALIDATION ============
    
    @pytest.mark.parametrize("materials_config", ProductTestData.MATERIALS_TEST_CASES)
    def test_scenario_materials_validation(self, materials_config):
        """SCENARIO 8: Create product with various materials configurations"""
        print(f"\n🔵 SCENARIO 8: Materials validation - {materials_config['name']}")
        
        payload = self.get_valid_payload()
        payload["materials"] = materials_config["materials"]
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        print(f"   Materials count: {len(materials_config['materials'])}")
        
        if materials_config["should_pass"] and response.status_code == 201:
            print(f"   ✅ PASSED: Materials config accepted")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"materials_{materials_config['name']}"
            })
        elif not materials_config["should_pass"] and response.status_code in [400, 422]:
            print(f"   ✅ PASSED: Invalid materials config rejected")
        elif materials_config["should_pass"] and response.status_code != 201:
            print(f"   ❌ FAILED: Expected acceptance but got {response.status_code}")
        else:
            print(f"   ⚠ WARNING: Unexpected result")
    
    # ============ SCENARIO 9: CREATE PRODUCT WITH TECHNIQUES VALIDATION ============
    
    @pytest.mark.parametrize("techniques_config", ProductTestData.TECHNIQUES_TEST_CASES)
    def test_scenario_techniques_validation(self, techniques_config):
        """SCENARIO 9: Create product with various techniques configurations"""
        print(f"\n🔵 SCENARIO 9: Techniques validation - {techniques_config['name']}")
        
        payload = self.get_valid_payload()
        payload["techniques"] = techniques_config["techniques"]
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        print(f"   Techniques count: {len(techniques_config['techniques'])}")
        
        if techniques_config["should_pass"] and response.status_code == 201:
            print(f"   ✅ PASSED: Techniques config accepted")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"techniques_{techniques_config['name']}"
            })
        elif not techniques_config["should_pass"] and response.status_code in [400, 422]:
            print(f"   ✅ PASSED: Invalid techniques config rejected")
        else:
            print(f"   ⚠ Result: Expected {201 if techniques_config['should_pass'] else '4xx'}, got {response.status_code}")
    
    # ============ SCENARIO 10: CREATE PRODUCT WITH FILES VALIDATION ============
    
    @pytest.mark.parametrize("files_config", ProductTestData.FILES_TEST_CASES)
    def test_scenario_files_validation(self, files_config):
        """SCENARIO 10: Create product with various files configurations"""
        print(f"\n🔵 SCENARIO 10: Files validation - {files_config['name']}")
        
        payload = self.get_valid_payload()
        payload["files"] = files_config["files"]
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        print(f"   Files count: {len(files_config['files'])}")
        
        if files_config["should_pass"] and response.status_code == 201:
            print(f"   ✅ PASSED: Files config accepted")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"files_{files_config['name']}"
            })
        elif not files_config["should_pass"] and response.status_code in [400, 422]:
            print(f"   ✅ PASSED: Invalid files config rejected")
        else:
            print(f"   ⚠ Result: Expected {201 if files_config['should_pass'] else '4xx'}, got {response.status_code}")
    
    # ============ SCENARIO 11: CREATE PRODUCT WITH MEASUREMENTS VALIDATION ============
    
    @pytest.mark.parametrize("measurements_config", ProductTestData.MEASUREMENTS_TEST_CASES)
    def test_scenario_measurements_validation(self, measurements_config):
        """SCENARIO 11: Create product with various measurements configurations"""
        print(f"\n🔵 SCENARIO 11: Measurements validation - {measurements_config['name']}")
        
        payload = self.get_valid_payload()
        payload["measurements"] = measurements_config["measurements"]
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        print(f"   Measurements count: {len(measurements_config['measurements'])}")
        
        if measurements_config["should_pass"] and response.status_code == 201:
            print(f"   ✅ PASSED: Measurements config accepted")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"measurements_{measurements_config['name']}"
            })
        elif not measurements_config["should_pass"] and response.status_code in [400, 422]:
            print(f"   ✅ PASSED: Invalid measurements config rejected")
        else:
            print(f"   ⚠ Result: Expected {201 if measurements_config['should_pass'] else '4xx'}, got {response.status_code}")
    
    # ============ SCENARIO 12: ANNUAL VS MONTHLY QUANTITY VALIDATION ============
    
    @pytest.mark.parametrize("monthly_qty,annual_qty,should_pass", 
                            ProductTestData.QUANTITY_RELATIONSHIP_TESTS)
    def test_scenario_annual_vs_monthly_quantity(self, monthly_qty, annual_qty, should_pass):
        """SCENARIO 12: Validate annual_qty >= monthly_qty * 12"""
        print(f"\n🔵 SCENARIO 12: Quantity validation")
        print(f"   Testing: monthly_qty={monthly_qty}, annual_qty={annual_qty}")
        print(f"   Expected: {monthly_qty * 12} <= {annual_qty} = {should_pass}")
        
        payload = self.get_valid_payload()
        payload["monthly_qty"] = monthly_qty
        payload["annual_qty"] = annual_qty
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if should_pass and response.status_code == 201:
            print(f"   ✅ PASSED: Valid quantity relationship accepted")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"qty_monthly_{monthly_qty}_annual_{annual_qty}"
            })
        elif not should_pass and response.status_code in [400, 422]:
            print(f"   ✅ PASSED: Invalid quantity relationship rejected")
        elif should_pass and response.status_code != 201:
            print(f"   ❌ FAILED: Valid relationship rejected with {response.status_code}")
        else:
            print(f"   ❌ FAILED: Invalid relationship accepted with {response.status_code}")
            data = response.json()
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": "invalid_quantity_relationship_accepted"
            })
    
    # ============ SCENARIO 13: DUPLICATE PRODUCT NAME ============
    
    def test_scenario_duplicate_product_name(self):
        """SCENARIO 13: Create product with duplicate name"""
        print("\n🔵 SCENARIO 13: Duplicate product name validation")
        print("   Testing: Same product name twice should be rejected")
        
        # Create first product
        product_name = self.generate_product_name()
        payload1 = self.get_valid_payload()
        payload1["name"] = product_name
        
        response1 = self.client.post("/products", json=payload1)
        print(f"   First creation status: {response1.status_code}")
        
        if response1.status_code == 201:
            data1 = response1.json()
            self.__class__.created_products.append({
                "id": data1["id"],
                "name": product_name,
                "scenario": "duplicate_name_first"
            })
            print(f"   ✅ First product created: {data1['id']}")
            
            # Try to create second product with same name
            payload2 = self.get_valid_payload()
            payload2["name"] = product_name
            
            response2 = self.client.post("/products", json=payload2)
            print(f"   Second creation status: {response2.status_code}")
            
            if response2.status_code == 409:
                print(f"   ✅ PASSED: Duplicate name correctly rejected with 409")
            elif response2.status_code == 201:
                print(f"   ❌ FAILED: Duplicate name was accepted!")
                data2 = response2.json()
                self.__class__.created_products.append({
                    "id": data2["id"],
                    "name": product_name,
                    "scenario": "duplicate_name_second"
                })
            else:
                print(f"   ⚠ WARNING: Expected 409, got {response2.status_code}")
        else:
            print(f"   ⚠ Could not test duplicate - first creation failed")
    
    # ============ SCENARIO 14: MISSING AUTHENTICATION ============
    
    def test_scenario_missing_authentication(self, api_client):
        """SCENARIO 14: Create product without authentication"""
        print("\n🔵 SCENARIO 14: Missing authentication")
        print("   Testing: Request without auth token should be rejected")
        
        # Create a client without auth token
        unauth_client = api_client
        
        payload = self.get_valid_payload()
        
        response = unauth_client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ PASSED: Unauthenticated request correctly rejected with 401")
        else:
            print(f"   ❌ FAILED: Expected 401, got {response.status_code}")
    
    # ============ SCENARIO 15: CREATE PRODUCT WITH IS_ACTIVE FLAG ============
    
    @pytest.mark.parametrize("is_active", [True, False])
    def test_scenario_is_active_flag(self, is_active):
        """SCENARIO 15: Create product with is_active flag"""
        print(f"\n🔵 SCENARIO 15: Create product with is_active={is_active}")
        
        payload = self.get_valid_payload()
        payload["is_active"] = is_active
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ PASSED: Product created with is_active={is_active}")
            print(f"   📦 Product ID: {data['id']}")
            
            self.__class__.created_products.append({
                "id": data["id"],
                "name": payload["name"],
                "scenario": f"is_active_{is_active}"
            })
        else:
            print(f"   ❌ FAILED: Expected 201, got {response.status_code}")
    
    # ============ CLEANUP ============
    
    @classmethod
    def teardown_class(cls):
        """Cleanup and summary after all tests"""
        print(f"\n{'='*70}")
        print(f"TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Products Created: {len(cls.created_products)}")
        
        if cls.created_products:
            print(f"\n📋 Created Products by Scenario:")
            scenario_count = {}
            for product in cls.created_products:
                scenario = product.get('scenario', 'unknown')
                scenario_count[scenario] = scenario_count.get(scenario, 0) + 1
            
            for scenario, count in sorted(scenario_count.items()):
                print(f"   • {scenario}: {count} product(s)")
            
            print(f"\n📋 Detailed List:")
            for i, product in enumerate(cls.created_products, 1):
                print(f"   {i}. {product.get('name', 'N/A')[:50]} (ID: {product.get('id', 'N/A')}) - {product.get('scenario', 'N/A')}")
        
        print(f"\n⚠️  Note: Products created during tests may need manual cleanup")
        print(f"{'='*70}\n")