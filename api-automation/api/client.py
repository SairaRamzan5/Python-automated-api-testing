import requests
import time
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or "https://api.uat.teresaapp.com/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # LARGE DELAY FOR UAT
        self.last_request_time = 0
        self.request_delay = 3.0  # 3 seconds
        
        logger.info(f"APIClient initialized for {self.base_url}")
    
    def _add_delay(self):
        """3 seconds delay between every request"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def request(self, method, endpoint, **kwargs):
        """Simple request with large delay"""
        self._add_delay()
        
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        logger.info(f"Request: {method} {url}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            logger.info(f"Response: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Error: {e}")
            raise
    
    # HTTP Methods - ADD THESE:
    def get(self, endpoint, **kwargs):
        return self.request('GET', endpoint, **kwargs)
    
    def post(self, endpoint, **kwargs):
        return self.request('POST', endpoint, **kwargs)
    
    def put(self, endpoint, **kwargs):  # ADD THIS METHOD
        return self.request('PUT', endpoint, **kwargs)
    
    def patch(self, endpoint, **kwargs):  # ADD THIS METHOD - THIS IS WHAT'S MISSING!
        return self.request('PATCH', endpoint, **kwargs)
    
    def delete(self, endpoint, **kwargs):  # You might need this too
        return self.request('DELETE', endpoint, **kwargs)
    
    # Auth methods
    def set_auth_token(self, token):
        self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def clear_auth_token(self):
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']