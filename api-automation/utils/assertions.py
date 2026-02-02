"""Assertion utilities for API testing"""

import json
import pytest

class Assertions:
    @staticmethod
    def assert_status_code(response, expected_code: int):
        """Assert that response has expected status code"""
        assert response.status_code == expected_code, \
            f"Expected status code {expected_code}, got {response.status_code}.\n" \
            f"Response: {response.text[:500]}"
    
    @staticmethod
    def assert_json_key_exists(response, key: str):
        """Assert that JSON response has specific key"""
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {response.text}")
        
        # Handle nested keys (e.g., "data.user.id")
        if '.' in key:
            keys = key.split('.')
            current = response_json
            for k in keys:
                assert k in current, f"Key '{k}' not found in path '{key}'"
                current = current[k]
        else:
            assert key in response_json, f"Key '{key}' not found in response"
    
    @staticmethod
    def assert_json_value(response, key: str, expected_value):
        """Assert that JSON response has specific value for key"""
        response_json = response.json()
        
        # Handle nested keys
        if '.' in key:
            keys = key.split('.')
            current = response_json
            for k in keys:
                if k not in current:
                    pytest.fail(f"Key '{k}' not found in path '{key}'")
                current = current[k]
            actual_value = current
        else:
            assert key in response_json, f"Key '{key}' not found in response"
            actual_value = response_json[key]
        
        assert actual_value == expected_value, \
            f"Expected {key}={expected_value}, got {actual_value}"
    
    @staticmethod
    def assert_response_contains(response, text: str):
        """Assert that response contains specific text"""
        assert text in response.text, \
            f"Expected text '{text}' not found in response"
    
    @staticmethod
    def assert_response_time(response, max_time_seconds: float = 5.0):
        """Assert that response time is within limit"""
        elapsed = response.elapsed.total_seconds()
        assert elapsed <= max_time_seconds, \
            f"Response time {elapsed:.2f}s exceeds limit {max_time_seconds}s"
    
    @staticmethod
    def assert_error_message(response, expected_message: str):
        """Assert that error response contains expected message"""
        try:
            response_json = response.json()
            actual_message = response_json.get("message", "")
            assert expected_message in actual_message, \
                f"Expected error message containing '{expected_message}', got '{actual_message}'"
        except json.JSONDecodeError:
            assert expected_message in response.text, \
                f"Expected error message '{expected_message}' not found in response"
    
    @staticmethod
    def assert_token_structure(token: str):
        """Assert JWT token has correct structure"""
        assert token is not None, "Token should not be None"
        assert len(token) > 50, f"Token seems too short: {len(token)} chars"
        
        # Check JWT structure (3 parts separated by dots)
        parts = token.split('.')
        assert len(parts) == 3, f"JWT token should have 3 parts, got {len(parts)}"
        
        # Check each part is base64 encoded
        import base64
        try:
            for i in range(2):  # Check header and payload
                # Add padding if needed
                part = parts[i]
                padding = 4 - len(part) % 4
                if padding != 4:
                    part += "=" * padding
                decoded = base64.b64decode(part)
                # Should be valid JSON
                json.loads(decoded)
        except Exception as e:
            pytest.fail(f"Invalid JWT token structure: {e}")
    
    @staticmethod
    def assert_user_data(user_data: dict):
        """Assert user data has required fields"""
        required_fields = ["id", "f_name", "l_name", "email"]
        optional_fields = ["phone_verified", "email_verified", "mfa_enabled"]
        
        for field in required_fields:
            assert field in user_data, f"User data missing required field: {field}"
            assert user_data[field] is not None, f"User.{field} should not be None"
        
        # ID should be UUID format
        import uuid
        try:
            uuid.UUID(user_data["id"])
        except ValueError:
            pytest.fail(f"User ID should be valid UUID, got: {user_data['id']}")
        
        # Email should be present (can be string)
        assert isinstance(user_data["email"], str), f"Email should be string, got {type(user_data['email'])}"
    
    @staticmethod
    def assert_success_response(response):
        """Assert response indicates success (200 or 204)"""
        assert response.status_code in [200, 204], \
            f"Expected status code 200 or 204, got {response.status_code}.\n" \
            f"Response: {response.text[:500]}"
        
        # For 204, there's no content to parse
        if response.status_code == 200:
            response_json = response.json()
            assert response_json.get("success") == True, \
                f"Response success should be True, got {response_json.get('success')}"
            assert "message" in response_json, "Response should have message field"
            assert "data" in response_json, "Response should have data field"
    
    @staticmethod
    def assert_validation_error(response):
        """Assert response is a validation error"""
        Assertions.assert_status_code(response, 422)
        response_json = response.json()
        assert response_json.get("success") == False, \
            "Validation error should have success=False"
        assert "errors" in response_json or "error" in response_json, \
            "Validation error should have errors or error field"
    
    @staticmethod
    def assert_unauthorized(response):
        """Assert response is unauthorized"""
        Assertions.assert_status_code(response, 401)
        response_json = response.json()
        assert response_json.get("success") == False, \
            "Unauthorized response should have success=False"