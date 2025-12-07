from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from .models import Book
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        # logic to create book
        return HttpResponse("Book Created")
    return HttpResponse("Create Book Page")

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # logic to edit book
        return HttpResponse("Book Edited")
    return HttpResponse(f"Edit Book {book.title}")

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return HttpResponse("Book Deleted")
    return HttpResponse(f"Delete Book {book.title}")

def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process form data securely
            return HttpResponse("Form Submitted Securely")
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

# Start of Selection
def book_search(request):
    query = request.GET.get('q')
    if query:
        # Secure: Using Django ORM filter prevents SQL injection
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
# End of Selection
