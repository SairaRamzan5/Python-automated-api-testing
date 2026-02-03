"""Test user manager - extracts user IDs from whitelist"""

import time
from config.register_test_data import generate_unique_email, generate_unique_phone
from api.endpoints import Endpoints
from config.settings import settings

class UserManager:
    """Manages test artisans - finds users in whitelist"""
    
    def __init__(self, api_client):
        self.client = api_client
        self.test_users = []  # Store created users
        self.admin_token = None
    
    def get_admin_token(self):
        """Get admin token for whitelist access"""
        if not self.admin_token:
            print("   Getting admin token...")
            login_data = {
                "identifier": settings.ADMIN_EMAIL,
                "password": settings.ADMIN_PASSWORD
            }
            
            response = self.client.post(Endpoints.LOGIN, json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.admin_token = data.get("data", {}).get("access_token")
                    print("   ✓ Admin token obtained")
                    return self.admin_token
                else:
                    print(f"   ❌ Admin login failed: {data.get('message')}")
            else:
                print(f"   ❌ Admin login HTTP error: {response.status_code}")
        
        return self.admin_token
    
    def create_test_artisan(self, approved=True):
        """Create a test artisan and find it in whitelist"""
        print(f"\n   Creating test artisan (approved={approved})...")
        
        # Generate unique test data
        email = generate_unique_email("test_artisan")
        phone = generate_unique_phone()
        password = "TestPassword123!"  # KNOWN PASSWORD
        
        print(f"   Email: {email}")
        print(f"   Phone: {phone}")
        print(f"   Password: {password}")
        
        # Create artisan data
        artisan_data = {
            "f_name": "Test",
            "l_name": "Artisan",
            "phone": phone,
            "email": email,
            "password": password
        }
        
        # Register the artisan
        response = self.client.post(Endpoints.REGISTER, json=artisan_data)
        
        if response.status_code == 201:
            print(f"   ✓ Test artisan created: {email}")
            
            # Store basic info
            user_info = {
                "email": email,
                "phone": phone,
                "password": password,
                "approved": False,
                "status": "pending_approval",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Wait for user to appear in whitelist
            print(f"   Waiting for user to appear in whitelist...")
            time.sleep(3.0)
            
            # Find user in whitelist to get the ID
            user_id = self.find_user_in_whitelist(email, phone)
            if user_id:
                user_info["id"] = user_id
                print(f"   ✓ Found user in whitelist: ID = {user_id}")
            else:
                print(f"   ⚠ User not found in whitelist yet")
                # Try again in 5 seconds
                time.sleep(5.0)
                user_id = self.find_user_in_whitelist(email, phone)
                if user_id:
                    user_info["id"] = user_id
                    print(f"   ✓ Found user in whitelist (retry): ID = {user_id}")
                else:
                    print(f"   ❌ Could not find user in whitelist")
            
            self.test_users.append(user_info)
            
            # Approve if requested AND we have user_id
            if approved and user_info.get("id"):
                print(f"\n   Attempting to approve user...")
                if self.approve_user_in_whitelist(user_info["id"]):
                    user_info["approved"] = True
                    user_info["status"] = "approved"
                    print(f"   ✓ Artisan approved in whitelist")
                else:
                    print(f"   ⚠ Artisan created but not approved")
            elif approved and not user_info.get("id"):
                print(f"   ⚠ Cannot approve: No user ID available")
            
            return user_info
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
    
    def find_user_in_whitelist(self, email, phone):
        """Find a user in whitelist by email or phone and return user ID"""
        admin_token = self.get_admin_token()
        if not admin_token:
            print(f"   ❌ Cannot search whitelist: No admin token")
            return None
        
        self.client.set_auth_token(admin_token)
        
        # Try searching by email
        if email:
            params = {"search": email, "page": 1, "limit": 10}
            response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
            
            if response.status_code == 200:
                data = response.json()
                users = data.get("data", [])
                
                for user in users:
                    if user.get("email") == email:
                        self.client.clear_auth_token()
                        return user.get("id")
        
        # Try searching by phone
        if phone:
            params = {"search": phone, "page": 1, "limit": 10}
            response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
            
            if response.status_code == 200:
                data = response.json()
                users = data.get("data", [])
                
                for user in users:
                    if user.get("phone") == phone:
                        self.client.clear_auth_token()
                        return user.get("id")
        
        self.client.clear_auth_token()
        return None
    
    def approve_user_in_whitelist(self, user_id):
        """Approve a user via whitelist approval endpoint"""
        admin_token = self.get_admin_token()
        if not admin_token:
            print(f"   ❌ Cannot approve: No admin token")
            return False
        
        print(f"   Using user_id for approval: {user_id}")
        
        # Validate UUID format
        import uuid
        try:
            uuid.UUID(user_id)
            print(f"   ✓ User ID is valid UUID")
        except ValueError:
            print(f"   ⚠ User ID is NOT a valid UUID: {user_id}")
            # Try to extract UUID if it's in a string
            import re
            uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
            match = re.search(uuid_pattern, user_id)
            if match:
                user_id = match.group(0)
                print(f"   Extracted UUID: {user_id}")
        
        self.client.set_auth_token(admin_token)
        
        approval_data = {
            "user_id": user_id,
            "status": "approved",
            "reason": "Test automation approval"
        }
        
        print(f"   Approval payload: {approval_data}")
        
        response = self.client.patch(Endpoints.WHITELIST_AUDIT, json=approval_data)
        
        self.client.clear_auth_token()
        
        if response.status_code == 200:
            print(f"   ✓ User approved: {user_id}")
            return True
        else:
            print(f"   ❌ Approval failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    
    def get_or_create_approved_user(self):
        """Get existing approved user or create new one"""
        print("\n   Getting/Creating approved user...")
        
        # Check existing approved users
        for user in self.test_users:
            if user.get("approved"):
                print(f"   ✓ Using existing approved user: {user['email']}")
                return user
        
        # Create new approved user
        print("   No existing approved user found, creating new one...")
        return self.create_test_artisan(approved=True)
    
    def get_or_create_pending_user(self):
        """Get existing pending user or create new one"""
        print("\n   Getting/Creating pending user...")
        
        # Check existing pending users
        for user in self.test_users:
            if not user.get("approved"):
                print(f"   ✓ Using existing pending user: {user['email']}")
                return user
        
        # Create new pending user
        print("   No existing pending user found, creating new one...")
        return self.create_test_artisan(approved=False)
    
    def find_recent_test_users_in_whitelist(self):
        """Find all test users in whitelist"""
        admin_token = self.get_admin_token()
        if not admin_token:
            print(f"   ❌ Cannot search whitelist: No admin token")
            return []
        
        self.client.set_auth_token(admin_token)
        
        # Search for test users
        params = {"search": "test_artisan", "page": 1, "limit": 20}
        response = self.client.get(Endpoints.WHITELIST_AUDIT, params=params)
        
        self.client.clear_auth_token()
        
        if response.status_code == 200:
            data = response.json()
            users = data.get("data", [])
            
            print(f"   Found {len(users)} test users in whitelist:")
            for user in users:
                status = user.get('status', 'unknown')
                approved = status == 'approved'
                print(f"   - {user.get('email')} ({status}) - ID: {user.get('id')}")
                
                # Update our test_users list
                for test_user in self.test_users:
                    if test_user.get('email') == user.get('email'):
                        test_user['id'] = user.get('id')
                        test_user['status'] = status
                        test_user['approved'] = approved
            
            return users
        
        return []