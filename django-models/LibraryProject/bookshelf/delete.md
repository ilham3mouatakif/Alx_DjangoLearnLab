# Delete Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
all_books = Book.objects.all()
print(all_books)
```

## Output
```
<QuerySet []>
```
