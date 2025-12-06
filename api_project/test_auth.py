import requests
import os
import django

# Setup Django standalone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()
username = 'testuser_api'
password = 'password123'

# Create user if not exists
if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(username=username, password=password)
    print(f"User {username} created.")
else:
    user = User.objects.get(username=username)
    print(f"User {username} already exists.")

# Test obtain token
url_token = 'http://127.0.0.1:8001/api/api-token-auth/'
response_token = requests.post(url_token, data={'username': username, 'password': password})
if response_token.status_code == 200:
    token = response_token.json().get('token')
    print(f"Token obtained: {token}")
else:
    print(f"Failed to obtain token: {response_token.status_code} {response_token.text}")
    exit(1)

# Test accessing protected endpoint without token
url_books = 'http://127.0.0.1:8001/api/books_all/'
response_no_token = requests.get(url_books)
print(f"Access without token: {response_no_token.status_code}") # Should be 401 or 403

# Test accessing protected endpoint with token
headers = {'Authorization': f'Token {token}'}
response_with_token = requests.get(url_books, headers=headers)
print(f"Access with token: {response_with_token.status_code}") # Should be 200
if response_with_token.status_code == 200:
    print("Content:", response_with_token.json())
else:
    print("Failed with token", response_with_token.text)
