# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

API_KEY = "YOUR_SECRET_KEY"  # Replace with a strong secret key

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.headers.get('X-API-KEY')
        if not key:
            return None  # Let DRF handle unauthenticated requests
        if key != API_KEY:
            raise AuthenticationFailed('Invalid API Key')
        return (None, None)  # No user associated, just key auth
