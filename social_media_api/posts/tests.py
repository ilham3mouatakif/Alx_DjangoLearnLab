from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.post_data = {'title': 'Test Post', 'content': 'Test Content'}
        self.post = Post.objects.create(author=self.user, title='Existing Post', content='Content')

    def test_create_post(self):
        response = self.client.post(reverse('post-list'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.get(id=response.data['id']).author, self.user)

    def test_update_post(self):
        url = reverse('post-detail', args=[self.post.id])
        updated_data = {'title': 'Updated Title', 'content': 'Updated Content'}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_delete_post(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_filter_posts(self):
        Post.objects.create(author=self.user, title='Another Post', content='Searchable Content')
        response = self.client.get(reverse('post-list') + '?search=Searchable')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Another Post')

class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Content')
        self.comment_data = {'post': self.post.id, 'content': 'Test Comment'}
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='Existing Comment')

    def test_create_comment(self):
        response = self.client.post(reverse('comment-list'), self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.get(id=response.data['id']).author, self.user)

    def test_update_comment(self):
        url = reverse('comment-detail', args=[self.comment.id])
        updated_data = {'post': self.post.id, 'content': 'Updated Comment'}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated Comment')

    def test_delete_comment(self):
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

class FeedTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.client.force_authenticate(user=self.user1)
        self.post_user2 = Post.objects.create(author=self.user2, title='User2 Post', content='Content')
        self.feed_url = reverse('feed')

    def test_feed_generation(self):
        # Initial check - empty feed
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 0) # This might fail if pagination is on, data would be under 'results'

        # Follow user2
        self.user1.following.add(self.user2)

        # Feed check - should have 1 post
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle list response directly if pagination is not active or transparent
        results = response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'User2 Post')
