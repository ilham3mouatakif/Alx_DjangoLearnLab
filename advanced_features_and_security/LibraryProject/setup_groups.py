import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

def setup_groups():
    # Define groups and their permissions
    groups_permissions = {
        'Editors': ['can_create', 'can_edit'],
        'Viewers': ['can_view'],
        'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
    }

    content_type = ContentType.objects.get_for_model(Book)

    for group_name, perms in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Created group: {group_name}")
        else:
            print(f"Group exists: {group_name}")

        for perm_codename in perms:
            try:
                permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
                group.permissions.add(permission)
                print(f"Added {perm_codename} to {group_name}")
            except Permission.DoesNotExist:
                print(f"Permission {perm_codename} not found!")
    
    print("Groups and permissions setup complete.")

if __name__ == '__main__':
    setup_groups()
