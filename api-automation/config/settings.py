"""Application settings for Teresa Backoffice UAT - FIXED VERSION"""

import os
import sys
from dotenv import load_dotenv

try:
    # Load environment variables with better error handling
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path, override=True)
    print(f"✓ Loaded environment variables from: {env_path}")
except Exception as e:
    print(f"⚠ Warning: Could not load .env file: {e}")
    print("⚠ Using default settings...")

class Settings:
    # API Configuration
    BASE_URL = os.getenv("BASE_URL", "https://api.uat.teresaapp.com/api/v1")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "uat").upper()
    
    # Test Configuration - OPTIMIZED FOR SPEED
    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "0.5"))  # Reduced from 1.0
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))  # Reduced from 30
    TEST_DELAY = float(os.getenv("TEST_DELAY", "0.3"))  # Reduced from 1.0
    
    # NEW: Rate limiting protection
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
    RATE_LIMIT_MAX_WAIT = int(os.getenv("RATE_LIMIT_MAX_WAIT", "60"))
    
    # Test Data - UAT Environment
    TEST_USER_IDENTIFIER = os.getenv("TEST_USER_IDENTIFIER", "admin")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "admin123")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", TEST_USER_IDENTIFIER)
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", TEST_USER_PASSWORD)
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", f"api_tests_{ENVIRONMENT.lower()}.log")
    ENABLE_PERFORMANCE_LOG = os.getenv("ENABLE_PERFORMANCE_LOG", "true").lower() == "true"
    
    # Reporting
    ALLURE_RESULTS = os.getenv("ALLURE_RESULTS", "./reports/allure-results")
    
    # UAT Specific Settings
    HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': f'Teresa-UAT-Test-Automation/1.0 ({ENVIRONMENT})',
        'X-Environment': ENVIRONMENT,
        'X-Request-Source': 'automation-tests'
    }
    
    # NEW: Endpoint specific settings
    ENDPOINT_CONFIG = {
        'auth': {
            'timeout': 15,
            'retries': 3,
            'delay': 0.5
        },
        'health': {
            'timeout': 5,
            'retries': 1,
            'delay': 0.1
        }
    }

settings = Settings()

# Print settings for debugging (optional)
if __name__ == "__main__":
    print(f"\nUAT Settings Loaded:")
    print(f"  BASE_URL: {settings.BASE_URL}")
    print(f"  ENVIRONMENT: {settings.ENVIRONMENT}")
    print(f"  REQUEST_DELAY: {settings.REQUEST_DELAY}s")
    print(f"  REQUEST_TIMEOUT: {settings.REQUEST_TIMEOUT}s")
    print(f"  MAX_RETRIES: {settings.MAX_RETRIES}")
    print(f"  TEST_USER: {settings.TEST_USER_IDENTIFIER}")