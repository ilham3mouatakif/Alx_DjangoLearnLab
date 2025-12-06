import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from bookshelf.models import Book

# Create
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Created: {book}")

# Retrieve
book = Book.objects.get(title="1984")
print(f"Retrieved: {book.title}, {book.author}, {book.publication_year}")

# Update
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated: {book.title}")

# Delete
book.delete()
print("Deleted")

# Verify Delete
try:
    Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    print("Confirmed Delete: Book does not exist")
