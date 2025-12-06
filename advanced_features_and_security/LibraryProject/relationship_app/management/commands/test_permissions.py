from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from relationship_app.models import Book

class Command(BaseCommand):
    help = 'Test permissions'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Create test users if they don't exist
        editor, _ = User.objects.get_or_create(username='editor_user', email='editor@example.com')
        viewer, _ = User.objects.get_or_create(username='viewer_user', email='viewer@example.com')
        admin_user, _ = User.objects.get_or_create(username='admin_user', email='admin@example.com')
        
        editor.set_password('password')
        viewer.set_password('password')
        admin_user.set_password('password')
        editor.save()
        viewer.save()
        admin_user.save()

        # Assign groups
        editors_group = Group.objects.get(name='Editors')
        viewers_group = Group.objects.get(name='Viewers')
        admins_group = Group.objects.get(name='Admins')

        editor.groups.add(editors_group)
        viewer.groups.add(viewers_group)
        admin_user.groups.add(admins_group)

        # Verify permissions
        self.stdout.write("Testing permissions...")
        
        def check_perm(user, perm):
            has_perm = user.has_perm(perm)
            self.stdout.write(f"User {user.username} has {perm}: {has_perm}")
            return has_perm

        # Editors should have add/change but MAYBE not delete (based on group setup)
        # In setup_groups: Editors: add, change. Viewers: view. Admins: add, change, delete, view.
        
        check_perm(editor, 'relationship_app.can_add_book')
        check_perm(editor, 'relationship_app.can_change_book')
        check_perm(editor, 'relationship_app.can_delete_book') # Should be False
        check_perm(editor, 'relationship_app.can_view_book')   # Should be False (unless implied? No)

        check_perm(viewer, 'relationship_app.can_view_book')
        check_perm(viewer, 'relationship_app.can_add_book')    # Should be False

        check_perm(admin_user, 'relationship_app.can_delete_book')
        check_perm(admin_user, 'relationship_app.can_view_book')

        self.stdout.write(self.style.SUCCESS('Permission testing script finished.'))
