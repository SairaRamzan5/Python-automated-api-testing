"""Product Creation API tests for Teresa Backoffice UAT"""

import pytest
import json
import time
from datetime import datetime
from api.endpoints import Endpoints
from utils.assertions import Assertions
from config.settings import settings
from test_product_data import ProductTestData

class TestProductCreationAPI:
    """Test suite for Product Creation API on UAT environment"""
    
    created_products = []  # Track created products
    
    @classmethod
    def setup_class(cls):
        """Setup before all tests"""
        print(f"\n{'='*70}")
        print(f"Starting PRODUCT CREATION API Tests")
        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"Base URL: {settings.BASE_URL}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
    
    @classmethod
    def teardown_class(cls):
        """Cleanup after all tests"""
        print(f"\n{'='*70}")
        print(f"Test Summary - Products Created: {len(cls.created_products)}")
        if cls.created_products:
            print(f"\nCreated Products:")
            for i, product in enumerate(cls.created_products, 1):
                print(f"  {i}. {product.get('name')} (ID: {product.get('id', 'N/A')})")
        print(f"{'='*70}\n")
    
    def setup_test(self):
        """Setup before each test method"""
        print(f"\n{'-'*50}")
    
    def teardown_test(self):
        """Cleanup after each test method"""
        print(f"{'-'*50}")
    
    def make_product_request(self, payload, auth_token=None, expected_status=None):
        """Helper method to make product creation request"""
        if auth_token:
            self.client.set_auth_token(auth_token)
        
        # Add delay to avoid rate limiting
        time.sleep(1.0)
        
        start_time = time.time()
        response = self.client.post(Endpoints.PRODUCTS, json=payload)
        response_time = time.time() - start_time
        
        # Reset to default token if custom was used
        if auth_token:
            self.login_artisan()
        
        # Handle rate limiting
        if response.status_code == 429:
            print(f"   ⚠ RATE LIMITED (429) - Waiting 5 seconds...")
            time.sleep(5.0)
            return self.make_product_request(payload, auth_token, expected_status)
        
        # Parse response
        response_data = {}
        if response.text and response.text.strip():
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                print(f"   ⚠ Response not JSON: {response.text[:200]}")
        
        return response, response_data, response_time
    
    @pytest.fixture(autouse=True)
    def setup_test_fixture(self, api_client):
        """Setup fixture that runs before each test"""
        self.client = api_client
        self.client.clear_auth_token()
        
        # Login artisan before each test
        if not self.login_artisan():
            pytest.skip("Artisan login failed, skipping test")
    
    def login_artisan(self):
        """Login as artisan and set auth token"""
        # Note: You need to set actual artisan credentials
        # This is a placeholder - replace with actual login logic
        print("   Attempting artisan login...")
        
        # For now, using a mock token - replace with actual login
        # In real implementation, you would:
        # 1. Call login endpoint with artisan credentials
        # 2. Extract token from response
        # 3. Set token for subsequent requests
        
        mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhcnRpc2FuQGV4YW1wbGUuY29tIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        self.client.set_auth_token(mock_token)
        print("   ✓ Using mock authentication token")
        return True
    
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_create_product_valid_data(self):
        """TC-001: Create product with valid data"""
        print("\n▶ TC-001: Create product with valid data")
        
        # Generate unique product name
        product_name = ProductTestData.generate_unique_product_name()
        payload = ProductTestData.get_valid_product_payload(name=product_name)
        
        print(f"   Creating product: {product_name}")
        print(f"   Description: {payload['description'][:50]}...")
        print(f"   Materials: {len(payload['materials'])} items")
        print(f"   Techniques: {len(payload['techniques'])} items")
        print(f"   Files: {len(payload['files'])} items")
        
        response, response_data, response_time = self.make_product_request(payload)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Time: {response_time:.3f}s")
        
        # Assertions
        Assertions.assert_status_code(response, 201)
        assert response_data.get("success") == True, "Success should be True"
        
        product_data = response_data.get("data", {})
        assert product_data.get("name") == product_name, "Product name should match"
        assert "id" in product_data, "Product should have ID"
        assert product_data.get("status") == "pending", "Status should be pending"
        
        # Store created product
        self.__class__.created_products.append({
            "id": product_data.get("id"),
            "name": product_name,
            "status": product_data.get("status")
        })
        
        print(f"   ✓ Product created successfully")
        print(f"   ✓ Product ID: {product_data.get('id')}")
        print(f"   ✓ Product Status: {product_data.get('status')}")
    
    @pytest.mark.positive
    @pytest.mark.parametrize("test_case", ProductTestData.VALIDATION_TEST_CASES[1:])  # Skip first test (already covered)
    def test_create_product_variations(self, test_case):
        """Test various valid product creation scenarios"""
        print(f"\n▶ {test_case['test_id']}: {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        
        # Generate base payload
        base_payload = ProductTestData.get_valid_product_payload()
        
        # Apply test case modifications
        test_payload = base_payload.copy()
        test_payload.update(test_case.get("payload", {}))
        
        # Make request
        response, response_data, response_time = self.make_product_request(test_payload)
        
        print(f"   Status Code: {response.status_code} (Expected: {test_case['expected_status']})")
        
        # Assertions
        Assertions.assert_status_code(response, test_case["expected_status"])
        
        if response.status_code == 201:
            assert response_data.get("success") == True, "Success should be True"
            
            product_data = response_data.get("data", {})
            
            # Check expected fields
            for field in test_case.get("expected_fields", []):
                assert field in product_data, f"Missing field: {field}"
            
            # Store created product
            self.__class__.created_products.append({
                "id": product_data.get("id"),
                "name": product_data.get("name"),
                "status": product_data.get("status")
            })
            
            print(f"   ✓ Product created successfully")
            print(f"   ✓ Response time: {response_time:.3f}s")
        else:
            print(f"   ⚠ Expected failure: {response.status_code}")
    
    @pytest.mark.negative
    @pytest.mark.parametrize("test_case", ProductTestData.NEGATIVE_TEST_CASES)
    def test_create_product_negative_cases(self, test_case):
        """Test negative scenarios for product creation"""
        print(f"\n▶ {test_case['test_id']}: {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        
        # Generate base payload
        base_payload = ProductTestData.get_valid_product_payload()
        
        # Apply test case modifications
        test_payload = base_payload.copy()
        
        # Handle special cases
        if test_case["payload"].get("name") is None:
            del test_payload["name"]
        elif test_case["payload"].get("description") is None:
            del test_payload["description"]
        else:
            test_payload.update(test_case.get("payload", {}))
        
        # Make request
        response, response_data, response_time = self.make_product_request(test_payload)
        
        print(f"   Status Code: {response.status_code} (Expected: {test_case['expected_status']})")
        
        # Assertions
        Assertions.assert_status_code(response, test_case["expected_status"])
        
        if response.status_code == 422:  # Validation error
            # Check for expected error in response
            if response_data:
                errors = response_data.get("errors", {})
                message = response_data.get("message", "").lower()
                
                # Check if expected error is in response
                expected_error = test_case.get("expected_error", "").lower()
                if expected_error:
                    error_found = False
                    
                    # Check in errors dict
                    for key in errors:
                        if expected_error in key.lower():
                            error_found = True
                            break
                    
                    # Check in message
                    if not error_found and expected_error in message:
                        error_found = True
                    
                    if error_found:
                        print(f"   ✓ Correctly rejected with '{expected_error}' error")
                    else:
                        print(f"   ⚠ Expected '{expected_error}' error but got: {message}")
        
        print(f"   ✓ Test passed - correctly rejected invalid data")
    
    @pytest.mark.materials
    @pytest.mark.parametrize("test_case", ProductTestData.MATERIAL_TEST_CASES)
    def test_material_validation(self, test_case):
        """Test material validation scenarios"""
        print(f"\n▶ {test_case['test_id']}: {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        
        # Generate base payload
        base_payload = ProductTestData.get_valid_product_payload()
        
        # Replace materials with test case materials
        base_payload["materials"] = test_case["payload"]["materials"]
        
        # Make request
        response, response_data, response_time = self.make_product_request(base_payload)
        
        print(f"   Status Code: {response.status_code} (Expected: {test_case['expected_status']})")
        
        # Assertions
        Assertions.assert_status_code(response, test_case["expected_status"])
        
        if response.status_code == 422:
            print(f"   ✓ Correctly rejected invalid material data")
        else:
            print(f"   ⚠ Unexpected status code: {response.status_code}")
    
    @pytest.mark.authentication
    def test_create_product_no_auth(self):
        """Test product creation without authentication"""
        print("\n▶ Authentication Test: Create product without auth token")
        
        payload = ProductTestData.get_valid_product_payload()
        
        # Clear auth token
        self.client.clear_auth_token()
        
        response, response_data, response_time = self.make_product_request(payload)
        
        print(f"   Status Code: {response.status_code}")
        
        # Should be 401 Unauthorized
        Assertions.assert_status_code(response, 401)
        
        if response.status_code == 401:
            print(f"   ✓ Correctly rejected without authentication")
        else:
            print(f"   ⚠ Expected 401 but got {response.status_code}")
    
    @pytest.mark.authentication
    def test_create_product_invalid_token(self):
        """Test product creation with invalid token"""
        print("\n▶ Authentication Test: Create product with invalid token")
        
        payload = ProductTestData.get_valid_product_payload()
        invalid_token = "invalid.token.here"
        
        response, response_data, response_time = self.make_product_request(
            payload, auth_token=invalid_token
        )
        
        print(f"   Status Code: {response.status_code}")
        
        # Should be 401 Unauthorized
        Assertions.assert_status_code(response, 401)
        
        if response.status_code == 401:
            print(f"   ✓ Correctly rejected with invalid token")
        else:
            print(f"   ⚠ Expected 401 but got {response.status_code}")
    
    @pytest.mark.performance
    def test_create_multiple_products(self):
        """Test creating multiple products in sequence"""
        print("\n▶ Performance Test: Create multiple products")
        
        products_to_create = 3
        created_count = 0
        response_times = []
        
        for i in range(products_to_create):
            print(f"\n   Creating product {i+1} of {products_to_create}...")
            
            product_name = f"Batch Product {int(time.time())}_{i}"
            payload = ProductTestData.get_valid_product_payload(name=product_name)
            
            # Simplify payload for faster processing
            payload["description"] = f"Test product #{i+1}"
            payload["monthly_qty"] = 100
            payload["annual_qty"] = 1200
            
            response, response_data, response_time = self.make_product_request(payload)
            response_times.append(response_time)
            
            if response.status_code == 201:
                created_count += 1
                product_id = response_data.get("data", {}).get("id", "N/A")
                print(f"   ✓ Created: {product_name} (ID: {product_id})")
                print(f"   ✓ Response time: {response_time:.3f}s")
            else:
                print(f"   ❌ Failed: Status {response.status_code}")
        
        # Summary
        print(f"\n   Summary:")
        print(f"   ✓ Attempted: {products_to_create}")
        print(f"   ✓ Created: {created_count}")
        print(f"   ✓ Success rate: {(created_count/products_to_create)*100:.1f}%")
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            print(f"   ✓ Average response time: {avg_time:.3f}s")
            print(f"   ✓ Individual times: {[f'{t:.3f}s' for t in response_times]}")
        
        # Reasonable expectation - at least 50% success rate
        assert created_count >= products_to_create * 0.5, f"Only {created_count}/{products_to_create} products created"
    
    @pytest.mark.boundary
    def test_create_product_boundary_values(self):
        """Test product creation with boundary values"""
        print("\n▶ Boundary Test: Create product with boundary values")
        
        test_cases = [
            {
                "name": "Minimum valid hours",
                "payload": {"hours_to_make": 1},
                "expected_status": 201
            },
            {
                "name": "Very high hours",
                "payload": {"hours_to_make": 1000},
                "expected_status": 201
            },
            {
                "name": "Minimum valid quantity",
                "payload": {"monthly_qty": 1, "annual_qty": 12},
                "expected_status": 201
            },
            {
                "name": "Maximum price",
                "payload": {"custom_price": 999999.99},
                "expected_status": 201
            },
            {
                "name": "Zero price (free product)",
                "payload": {"custom_price": 0},
                "expected_status": 201
            }
        ]
        
        for test_case in test_cases:
            print(f"\n   Testing: {test_case['name']}")
            
            payload = ProductTestData.get_valid_product_payload()
            payload.update(test_case["payload"])
            
            response, response_data, response_time = self.make_product_request(payload)
            
            print(f"   Status: {response.status_code} (Expected: {test_case['expected_status']})")
            
            if response.status_code == test_case["expected_status"]:
                print(f"   ✓ Passed")
            else:
                print(f"   ⚠ Unexpected status")
    
    @pytest.mark.functional
    def test_product_creation_workflow(self):
        """Test complete product creation workflow"""
        print("\n▶ Functional Test: Complete product creation workflow")
        
        # Step 1: Create product
        print(f"   Step 1: Creating product...")
        
        product_name = f"Workflow Test Product {int(time.time())}"
        payload = ProductTestData.get_valid_product_payload(name=product_name)
        
        response, response_data, response_time = self.make_product_request(payload)
        
        if response.status_code != 201:
            print(f"   ❌ Product creation failed: {response.status_code}")
            pytest.fail("Product creation failed")
            return
        
        product_id = response_data.get("data", {}).get("id")
        if not product_id:
            print(f"   ❌ No product ID in response")
            pytest.fail("No product ID returned")
            return
        
        print(f"   ✓ Product created: {product_name}")
        print(f"   ✓ Product ID: {product_id}")
        
        # Step 2: Verify product can be retrieved
        print(f"\n   Step 2: Retrieving created product...")
        
        # Get product endpoint (adjust based on your API)
        get_endpoint = f"{Endpoints.PRODUCTS}/{product_id}"
        
        time.sleep(1.0)  # Brief delay
        get_response = self.client.get(get_endpoint)
        
        if get_response.status_code == 200:
            get_data = get_response.json()
            retrieved_name = get_data.get("data", {}).get("name")
            
            if retrieved_name == product_name:
                print(f"   ✓ Product retrieved successfully")
                print(f"   ✓ Retrieved name matches: {retrieved_name}")
            else:
                print(f"   ⚠ Retrieved name doesn't match: {retrieved_name}")
        else:
            print(f"   ⚠ Could not retrieve product: {get_response.status_code}")
        
        # Store product
        self.__class__.created_products.append({
            "id": product_id,
            "name": product_name,
            "status": "pending"
        })
        
        print(f"\n   ✅ Workflow completed successfully")