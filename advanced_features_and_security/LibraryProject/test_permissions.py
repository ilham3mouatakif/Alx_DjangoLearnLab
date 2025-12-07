import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from bookshelf.models import Book

User = get_user_model()

def verify_permissions():
    print("Verifying Permissions...")
    # Create test users
    editor_user, _ = User.objects.get_or_create(username='editor', email='editor@example.com')
    editor_user.set_password('password')
    editor_user.save()
    viewer_user, _ = User.objects.get_or_create(username='viewer', email='viewer@example.com')
    viewer_user.set_password('password')
    viewer_user.save()
    admin_user, _ = User.objects.get_or_create(username='admin', email='admin@example.com')
    admin_user.set_password('password')
    admin_user.save()

    # Assign groups
    editor_group = Group.objects.get(name='Editors')
    viewer_group = Group.objects.get(name='Viewers')
    admin_group = Group.objects.get(name='Admins')

    editor_user.groups.add(editor_group)
    viewer_user.groups.add(viewer_group)
    admin_user.groups.add(admin_group)

    # Create a dummy book
    book, _ = Book.objects.get_or_create(title="Test Book", author="Test Author", publication_year=2024)

    client = Client()

    # Test Cases
    # Format: (User, URL, Expected Status Code)
    # Viewers: Can View (200), Cannot Create (403), Cannot Edit (403), Cannot Delete (403)
    # Editors: Can View (403? No, Editors don't have can_view explicitly in script? Let's check script), Can Create (200), Can Edit (200)
    # Admins: Can All (200)

    # Wait, my setup_groups script gave:
    # Editors: can_create, can_edit. (Missing can_view?)
    # Viewers: can_view.
    # Admins: all.
    
    # If Editors don't have can_view, they might fail book_list if it requires can_view. 
    # Let's see what happens. If they fail, I might need to add can_view to Editors too, or assume strict separation.
    # The prompt said: "Editors might have can_edit and can_create permissions." It didn't explicitly say they can view, but usually they should.
    # I will test strictly based on what I assigned.

    test_cases = [
        ('viewer', '/books/', 200),
        ('viewer', '/books/create/', 403),
        ('viewer', f'/books/{book.pk}/edit/', 403),
        ('viewer', f'/books/{book.pk}/delete/', 403),

        ('editor', '/books/create/', 200), # POST would be better but GET returns 200 if allowed
        ('editor', f'/books/{book.pk}/edit/', 200),
        # ('editor', '/books/', 403), # Expect 403 if they don't have can_view
        
        ('admin', '/books/', 200),
        ('admin', '/books/create/', 200),
        ('admin', f'/books/{book.pk}/edit/', 200),
        ('admin', f'/books/{book.pk}/delete/', 200),
    ]

    for username, url, expected_status in test_cases:
        client.login(username=username, password='password')
        response = client.get(url, secure=True)
        if response.status_code == expected_status:
            print(f"PASS: {username} accessing {url} returned {response.status_code}")
        else:
            print(f"FAIL: {username} accessing {url} returned {response.status_code}, expected {expected_status}")
            if response.status_code == 302: # Redirect to login usually means permission denied with standard decorators if using login_required, but permission_required raises 403 or redirects.
                 print(f"      Redirected to: {response.url}")

    print("Verification Complete.")

if __name__ == '__main__':
    verify_permissions()
