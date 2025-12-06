# CRUD Operations

## 1. Create
```python
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```
Output: `1984 by George Orwell`

## 2. Retrieve
```python
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
```
Output: `1984 George Orwell 1949`

## 3. Update
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
```
Output: `Nineteen Eighty-Four`

## 4. Delete
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
```
Output: `(1, {'bookshelf.Book': 1})`
