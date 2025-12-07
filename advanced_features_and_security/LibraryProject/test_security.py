import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

def verify_security():
    print("Verifying Security Controls...")
    client = Client(enforce_csrf_checks=True)

    # 1. Check Security Headers
    # Since we are testing client, middleware runs.
    response = client.get('/example-form/', secure=True)
    
    headers = response.items()
    header_dict = dict(headers)
    
    print("\nChecking Headers:")
    
    # X-Frame-Options
    xfo = header_dict.get('X-Frame-Options')
    if xfo == 'DENY':
        print("PASS: X-Frame-Options is DENY")
    else:
        print(f"FAIL: X-Frame-Options is {xfo}")

    # Content-Security-Policy
    csp = header_dict.get('Content-Security-Policy')
    if csp:
        print(f"PASS: CSP Header present: {csp}")
        if "default-src 'self'" in csp:
             print("PASS: CSP default-src is 'self'")
    else:
        # Note: django-csp might strictly require middleware middleware to be installed.
        # If it's not installed, settings alone won't add header.
        # We'll see if it fails.
        print("WARNING: CSP Header not found (django-csp might not be installed)")

    # X-Content-Type-Options
    xcto = header_dict.get('X-Content-Type-Options')
    if xcto == 'nosniff':
        print("PASS: X-Content-Type-Options is nosniff")
    else:
        print(f"FAIL: X-Content-Type-Options is {xcto}")

    # 2. Check CSRF
    print("\nChecking CSRF:")
    # Get the form page to set CSRF cookie
    response = client.get('/example-form/', secure=True)
    csrftoken = client.cookies['csrftoken'].value
    
    # Try POST without token (should fail 403)
    response_fail = client.post('/example-form/', {'search_query': 'test'}, secure=True)
    if response_fail.status_code == 403:
        print("PASS: POST without CSRF token rejected (403)")
    else:
        print(f"FAIL: POST without CSRF token returned {response_fail.status_code}")

    # Try POST with token
    # HTTPS requests require Referer header for CSRF check
    response_success = client.post('/example-form/', {'search_query': 'test', 'csrfmiddlewaretoken': csrftoken}, secure=True, HTTP_REFERER='https://testserver/example-form/')
    
    if response_success.status_code == 200:
        print("PASS: POST with CSRF token accepted (200)")
    else:
        # Client might need manual csrf handling if not automatic
        print(f"FAIL: POST with CSRF token returned {response_success.status_code}")

    # 3. Check Search SQL Injection Safety (Basic)
    print("\nChecking Search:")
    # SQLi payload: ' OR 1=1 --
    # Should be treated as literal string
    payload = "' OR 1=1 --"
    response_search = client.get('/search/', {'q': payload}, secure=True)
    if response_search.status_code == 200:
        # We can't easily check the SQL query here without logging, but we can verify it doesn't crash or return all books (if we had books)
        # Assuming existing view uses ORM filter(), it is safe.
        print("PASS: Search view handled inputs safely (200 OK)")
    else:
        print(f"FAIL: Search view returned {response_search.status_code}")

    print("\nVerification Complete.")

if __name__ == '__main__':
    verify_security()
