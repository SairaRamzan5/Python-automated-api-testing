class Endpoints:
    # Authentication endpoints
    LOGIN = "/auth/login"
    LOGOUT = "/auth/"
    REGISTER = "/auth/register"  # FIXED: Removed duplicate /api/v1
    REFRESH_TOKEN = "/auth/refresh"
    VERIFY_TOKEN = "/auth/verify"
    
    # User endpoints
    PROFILE = "/users/profile"
    USERS = "/users"
    USER_BY_ID = "/users/{user_id}"
    
    # Admin endpoints
    ADMIN_USERS = "/admin/users"
    ADMIN_DASHBOARD = "/admin/dashboard"

    # TECHNIQUES endpoints
    TECHNIQUES = "/techniques/"
    TECHNIQUES_UPDATE = "/rbac/techniques/update" 
    
    # Utility endpoints
    HEALTH = "/health"
    STATUS = "/status"
    METRICS = "/metrics"
    
    # Artisan-specific endpoints
    ARTISAN_PROFILE = "/artisans/profile"
    ARTISAN_SERVICES = "/artisans/services"
    
    # Verification endpoints
    VERIFY_EMAIL = "/auth/verify-email"
    VERIFY_PHONE = "/auth/verify-phone"
    RESEND_VERIFICATION = "/auth/resend-verification"

    # Whitelisting endpoints
    WHITELIST_AUDIT = "/whitelist-audit/" 
    WHITELIST_APPROVE = "/whitelist-audit/{id}/approve"  # If exists
    WHITELIST_REJECT = "/whitelist-audit/{id}/reject"    # If exists

    PRODUCTS = "/products"  # Add this line
    
    # Techniques
    TECHNIQUES = "/techniques/"
    
    # Files
    FILES = "/files/"
    
    # Units
    UNITS = "/units/"
    
    # Helper methods
    @staticmethod
    def user_detail(user_id: str) -> str:
        """Get user detail endpoint"""
        return Endpoints.USER_BY_ID.replace("{user_id}", user_id)
    
    @staticmethod
    def artisan_detail(artisan_id: str) -> str:
        """Get artisan detail endpoint"""
        return "/artisans/{artisan_id}".replace("{artisan_id}", artisan_id)


