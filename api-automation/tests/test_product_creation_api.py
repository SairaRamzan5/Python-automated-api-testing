"""Product Creation API tests for Artisans - CORRECTED STRUCTURE"""

import pytest
import json
import time
import uuid
from datetime import datetime
from config.test_product_data import ProductTestData

class TestArtisanProductCreation:
    """Test suite for Product Creation API - Artisans Only"""
    
    created_products = []  # Track created products
    
    @classmethod
    def setup_class(cls):
        """Setup before all tests"""
        print(f"\n{'='*70}")
        print(f"ARTISAN PRODUCT CREATION TESTS")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, artisan_auth_token):
        """Setup before each test"""
        self.client = api_client
        
        if not artisan_auth_token:
            pytest.skip("Artisan authentication required")
        
        self.client.set_auth_token(artisan_auth_token)
        print("   ✓ Artisan authentication set")
    
    def generate_product_name(self):
        """Generate unique product name"""
        unique_id = str(uuid.uuid4())[:6]
        timestamp = int(time.time())
        return f"Product {timestamp}-{unique_id}"
    
    @pytest.mark.smoke
    def test_create_product_correct_structure(self):
        """Test creating product with correct structure"""
        print("\n▶ Test: Create product with correct structure")
        
        product_name = self.generate_product_name()
        
        # CORRECT payload structure
        payload = {
            "name": product_name,
            "description": "Handmade product by artisan",
            "hours_to_make": 2.0,
            "monthly_qty": 100,
            "annual_qty": 1200,
            "custom_price": 29.99,
            "is_active": True,
            "status": "pending",
            "workshops": [],
            "materials": [
                {
                    "name": "Test Material",
                    "price": 50.0,
                    "quantity": 2,
                    "unit_id": "64b45044-ebf6-4290-8820-eaf04c109bd0"
                }
            ],
            "techniques": [  # CORRECT: Array of objects
                {
                    "id": "fcae2e4e-b8b5-4a5f-b879-111896c2e849"
                }
            ],
            "files": [  # CORRECT: Array of objects
                {
                    "id": "58a82002-020b-4e12-917f-5fcb3dccd29d"
                }
            ]
        }
        
        print(f"   Creating: {product_name}")
        print(f"   Structure: techniques (array of objects), files (array of objects)")
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ SUCCESS! Product created!")
            print(f"   Message: {data.get('message')}")
            
            product_id = data.get('data', {}).get('id')
            if product_id:
                self.__class__.created_products.append({
                    "id": product_id,
                    "name": product_name,
                    "status": data.get('data', {}).get('status', 'pending')
                })
                print(f"   Product ID: {product_id}")
        elif response.status_code == 422:
            data = response.json()
            print(f"   ⚠ Validation errors:")
            for error in data.get("errors", []):
                print(f"     - {error.get('field')}: {error.get('message')}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:200]}")
    
    @pytest.mark.positive
    def test_create_product_using_test_data(self):
        """Test creating product using the test data helper"""
        print("\n▶ Test: Create product using test data")
        
        payload = ProductTestData.get_valid_product_payload()
        product_name = payload["name"]
        
        print(f"   Creating: {product_name}")
        print(f"   Techniques: {len(payload.get('techniques', []))}")
        print(f"   Files: {len(payload.get('files', []))}")
        print(f"   Materials: {len(payload.get('materials', []))}")
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Product created successfully!")
            print(f"   Message: {data.get('message')}")
            
            product_id = data.get('data', {}).get('id')
            if product_id:
                self.__class__.created_products.append({
                    "id": product_id,
                    "name": product_name,
                    "status": data.get('data', {}).get('status', 'pending')
                })
        elif response.status_code == 422:
            data = response.json()
            print(f"   ⚠ Validation errors:")
            for error in data.get("errors", []):
                print(f"     - {error.get('field')}: {error.get('message')}")
    
    @pytest.mark.negative
    def test_create_product_name_too_long(self):
        """Test product name exceeds 30 characters"""
        print("\n▶ Test: Product name > 30 characters")
        
        long_name = "This is a very long product name that exceeds 30 characters limit"
        payload = ProductTestData.get_valid_product_payload(name=long_name)
        
        print(f"   Name length: {len(long_name)} characters")
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 422:
            data = response.json()
            print(f"   ✅ Correctly rejected with validation error")
            for error in data.get("errors", []):
                if "name" in error.get("field", "").lower():
                    print(f"   Name error: {error.get('message')}")
        else:
            print(f"   ⚠ Expected 422 but got {response.status_code}")
    
    @pytest.mark.negative
    def test_create_product_empty_materials(self):
        """Test product with empty materials array"""
        print("\n▶ Test: Empty materials array")
        
        payload = ProductTestData.get_valid_product_payload()
        payload["materials"] = []  # Empty materials
        
        response = self.client.post("/products", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 422:
            data = response.json()
            print(f"   ✅ Correctly rejected with validation error")
            for error in data.get("errors", []):
                if "materials" in error.get("field", "").lower():
                    print(f"   Materials error: {error.get('message')}")
    
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

        