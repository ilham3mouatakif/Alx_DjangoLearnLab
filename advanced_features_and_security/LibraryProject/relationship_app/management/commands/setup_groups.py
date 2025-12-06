from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

class Command(BaseCommand):
    help = 'Setup user groups and permissions'

    def handle(self, *args, **kwargs):
        # Define groups
        groups = {
            'Editors': ['can_add_book', 'can_change_book'],
            'Viewers': ['can_view_book'],
            'Admins': ['can_add_book', 'can_change_book', 'can_delete_book', 'can_view_book'],
        }

        for group_name, perms in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in perms:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission {perm_codename} not found'))
            
            self.stdout.write(self.style.SUCCESS(f'Group {group_name} setup successfully'))
