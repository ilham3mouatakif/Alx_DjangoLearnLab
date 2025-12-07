import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from bookshelf.models import CustomUser
from datetime import date

def test_custom_user():
    print("Testing CustomUser creation...")
    try:
        # Clean up if exists
        CustomUser.objects.filter(username='testuser').delete()
        CustomUser.objects.filter(username='superuser').delete()

        # Test create_user
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            date_of_birth=date(1990, 1, 1)
        )
        print(f"User created: {user.username}, DOB: {user.date_of_birth}")
        assert user.date_of_birth == date(1990, 1, 1)
        assert user.check_password('password123')

        # Test create_superuser
        superuser = CustomUser.objects.create_superuser(
            username='superuser',
            email='admin@example.com',
            password='adminpassword',
            date_of_birth=date(1980, 1, 1)
        )
        print(f"Superuser created: {superuser.username}, Is Staff: {superuser.is_staff}, Is Superuser: {superuser.is_superuser}")
        assert superuser.is_staff
        assert superuser.is_superuser

        print("All tests passed successfully!")

    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == '__main__':
    test_custom_user()
