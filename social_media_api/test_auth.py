import requests

BASE_URL = 'http://127.0.0.1:8000/api/users/'

def test_register():
    print("Testing Registration...")
    response = requests.post(f'{BASE_URL}register/', data={
        'username': 'testuser',
        'password': 'testpassword123',
        'bio': 'I am a test user'
    })
    print(response.status_code)
    print(response.json())
    return response.json().get('token')

def test_login():
    print("Testing Login...")
    response = requests.post(f'{BASE_URL}login/', data={
        'username': 'testuser',
        'password': 'testpassword123'
    })
    print(response.status_code)
    print(response.json())
    return response.json().get('token')

def test_profile(token):
    print("Testing Profile...")
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}profile/', headers=headers)
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    # Ensure server is running before executing this
    try:
        token = test_register()
        if not token:
            token = test_login()
        if token:
            test_profile(token)
    except Exception as e:
        print(e)
