# Permissions and Groups Setup

This Django application uses custom permissions and groups to manage access control.

## Custom Permissions
Defined in `bookshelf/models.py` on the `Book` model:
- `bookshelf.can_view`: Allows viewing book lists and details.
- `bookshelf.can_create`: Allows creating new books.
- `bookshelf.can_edit`: Allows editing existing books.
- `bookshelf.can_delete`: Allows deleting books.

## Groups
Three groups are configured with specific permissions:

1.  **Viewers**:
    - Permissions: `can_view`
    - Access: Can only view the list of books.

2.  **Editors**:
    - Permissions: `can_create`, `can_edit`
    - Access: Can create and edit books. cannot delete. (Note: Ensure they also have `can_view` if they need to see lists).

3.  **Admins**:
    - Permissions: `can_view`, `can_create`, `can_edit`, `can_delete`
    - Access: Full control over books.

## Configuration Script
A script `setup_groups.py` is provided to automatically create these groups and assign permissions.
Run it using:
```bash
python setup_groups.py
```

## Testing
To verify permissions, run:
```bash
python test_permissions.py
```
This script creates test users for each group and verifies their access to the protected views.
