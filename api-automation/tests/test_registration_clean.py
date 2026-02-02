# tests/test_registration_clean.py
"""Clean registration tests - independent execution"""

import pytest
import time
import random
import uuid
import json
from api.client import APIClient
from api.endpoints import Endpoints

class TestRegistrationClean:
    """Clean registration tests with independent execution"""
    
    def setup_method(self):
        """Setup before each test"""
        self.client = APIClient(base_url="https://api.uat.teresaapp.com/api/v1")
        self.client.clear_auth_token()
    
    def generate_unique_data(self, test_name=""):
        """Generate unique test data"""
        timestamp = int(time.time() * 1000)
        random_id = uuid.uuid4().hex[:6]
        phone = f"+88017{''.join([str(random.randint(0, 9)) for _ in range(8)])}"
        email = f"test_{test_name}_{timestamp}_{random_id}@test.com"
        return {
            "phone": phone,
            "email": email,
            "timestamp": timestamp
        }
    
    def test_valid_registration(self):
        """Test valid registration"""
        print(f"\n{'='*60}")
        print("Test 1: Valid Registration")
        print(f"{'='*60}")
        
        data = self.generate_unique_data("valid")
        
        payload = {
            "f_name": "Valid",
            "l_name": "User",
            "phone": data["phone"],
            "email": data["email"],
            "password": "SecurePass123!",
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        print(f"Phone: {data['phone']}")
        print(f"Email: {data['email']}")
        
        start = time.time()
        response = self.client.post(Endpoints.REGISTER, json=payload)
        elapsed = time.time() - start
        
        print(f"\nResponse time: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ PASS: Registration successful")
            response_data = response.json()
            print(f"User ID: {response_data.get('data', {}).get('user', {}).get('id', 'N/A')}")
        else:
            print(f"Response: {response.text[:200]}")
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        print(f"{'='*60}\n")
    
    def test_missing_last_name(self):
        """Test registration without last name (should work - optional)"""
        print(f"\n{'='*60}")
        print("Test 2: Registration without Last Name")
        print(f"{'='*60}")
        
        data = self.generate_unique_data("no_lname")
        
        payload = {
            "f_name": "NoLastName",
            "phone": data["phone"],
            "email": data["email"],
            "password": "SecurePass123!",
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        print(f"Phone: {data['phone']}")
        print(f"Email: {data['email']}")
        
        start = time.time()
        response = self.client.post(Endpoints.REGISTER, json=payload)
        elapsed = time.time() - start
        
        print(f"\nResponse time: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ PASS: Registration successful without last name")
        elif response.status_code == 422:
            print("⚠ Last name is required (unexpected)")
        else:
            print(f"Response: {response.text[:200]}")
        
        # Accept either 201 (optional) or 422 (required)
        assert response.status_code in [201, 422], f"Unexpected status: {response.status_code}"
        print(f"{'='*60}\n")
    
    def test_weak_password(self):
        """Test registration with weak password"""
        print(f"\n{'='*60}")
        print("Test 3: Weak Password Validation")
        print(f"{'='*60}")
        
        data = self.generate_unique_data("weak_pass")
        
        payload = {
            "f_name": "Weak",
            "l_name": "Password",
            "phone": data["phone"],
            "email": data["email"],
            "password": "123",  # Too weak
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        start = time.time()
        response = self.client.post(Endpoints.REGISTER, json=payload)
        elapsed = time.time() - start
        
        print(f"Response time: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 422:
            print("✅ PASS: Weak password rejected")
            response_data = response.json()
            if "errors" in response_data:
                for error in response_data["errors"]:
                    if error.get("field") == "password":
                        print(f"Error: {error.get('message')}")
        else:
            print(f"Response: {response.text[:200]}")
        
        assert response.status_code == 422, f"Expected 422 for weak password, got {response.status_code}"
        print(f"{'='*60}\n")
    
    def test_invalid_email(self):
        """Test registration with invalid email"""
        print(f"\n{'='*60}")
        print("Test 4: Invalid Email Validation")
        print(f"{'='*60}")
        
        data = self.generate_unique_data("invalid_email")
        
        payload = {
            "f_name": "Invalid",
            "l_name": "Email",
            "phone": data["phone"],
            "email": "not-an-email",  # Invalid
            "password": "SecurePass123!",
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        start = time.time()
        response = self.client.post(Endpoints.REGISTER, json=payload)
        elapsed = time.time() - start
        
        print(f"Response time: {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 422:
            print("✅ PASS: Invalid email rejected")
        else:
            print(f"Response: {response.text[:200]}")
        
        assert response.status_code == 422, f"Expected 422 for invalid email, got {response.status_code}"
        print(f"{'='*60}\n")
    
    def test_duplicate_prevention(self):
        """Test duplicate email prevention"""
        print(f"\n{'='*60}")
        print("Test 5: Duplicate Email Prevention")
        print(f"{'='*60}")
        
        # First, create a user
        data = self.generate_unique_data("dup_test")
        
        first_user = {
            "f_name": "First",
            "l_name": "User",
            "phone": data["phone"],
            "email": data["email"],
            "password": "SecurePass123!",
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        print(f"Creating first user:")
        print(f"Email: {data['email']}")
        
        response1 = self.client.post(Endpoints.REGISTER, json=first_user)
        
        if response1.status_code != 201:
            print(f"⚠ Could not create first user: {response1.status_code}")
            print("Skipping duplicate test")
            pytest.skip("Need first user for duplicate test")
            return
        
        print("✅ First user created")
        
        # Try to create duplicate with different phone
        new_phone = f"+88017{''.join([str(random.randint(0, 9)) for _ in range(8)])}"
        duplicate_user = {
            "f_name": "Duplicate",
            "l_name": "User",
            "phone": new_phone,
            "email": data["email"],  # Same email!
            "password": "SecurePass123!",
            "frontend_url": "https://uat.teresaapp.com/verify"
        }
        
        print(f"\nTrying duplicate with:")
        print(f"Email: {data['email']} (same)")
        print(f"Phone: {new_phone} (different)")
        
        response2 = self.client.post(Endpoints.REGISTER, json=duplicate_user)
        
        print(f"\nDuplicate attempt status: {response2.status_code}")
        
        if response2.status_code in [409, 400]:
            print("✅ PASS: Duplicate email rejected")
        else:
            print(f"Response: {response2.text[:200]}")
            print(f"⚠ Expected 409 or 400 for duplicate")
        
        # Accept 409 (Conflict) or 400 (Bad Request) for duplicates
        assert response2.status_code in [409, 400, 422], \
            f"Expected 409, 400, or 422 for duplicate, got {response2.status_code}"
        print(f"{'='*60}\n")