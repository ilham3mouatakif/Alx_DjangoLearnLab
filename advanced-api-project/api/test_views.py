from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author
from django.urls import reverse

class BookAPITests(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create author
        self.author = Author.objects.create(name="Test Author")
        
        # Create books
        self.book1 = Book.objects.create(title="Book One", publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2021, author=self.author)
        
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.detail_url = lambda pk: reverse('book-detail', args=[pk])
        self.update_url = lambda pk: reverse('book-update', args=[pk])
        self.delete_url = lambda pk: reverse('book-delete', args=[pk])

    def test_list_books(self):
        """Test retrieving list of books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        """Test creating a book with authentication"""
        self.client.login(username='testuser', password='password')
        data = {'title': 'New Book', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication (should fail)"""
        data = {'title': 'New Book', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        """Test updating a book"""
        self.client.login(username='testuser', password='password')
        data = {'title': 'Updated Book One', 'publication_year': 2020, 'author': self.author.id}
        response = self.client.put(self.update_url(self.book1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')

    def test_delete_book(self):
        """Test deleting a book"""
        self.client.login(username='testuser', password='password')
        response = self.client.delete(self.delete_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books(self):
        """Test filtering books by title"""
        response = self.client.get(self.list_url, {'title': 'Book One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_search_books(self):
        """Test searching books"""
        response = self.client.get(self.list_url, {'search': 'One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_order_books(self):
        """Test ordering books"""
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book Two') # 2021 > 2020
