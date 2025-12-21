from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = User.objects.create_user(username='author', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(author=self.author, title='Test Post', content='Content')
        self.like_url = reverse('like_post', args=[self.post.pk])
        self.unlike_url = reverse('unlike_post', args=[self.post.pk])

    def test_like_post(self):
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.author)
        self.assertEqual(notification.actor, self.user)
        self.assertEqual(notification.verb, 'liked')

    def test_like_post_twice(self):
        self.client.post(self.like_url)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 1)

    def test_unlike_post(self):
        self.client.post(self.like_url)
        response = self.client.post(self.unlike_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

    def test_unlike_not_liked_post(self):
        response = self.client.post(self.unlike_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class NotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.actor = User.objects.create_user(username='actor', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.notification = Notification.objects.create(
            recipient=self.user,
            actor=self.actor,
            verb='test notification'
        )
        self.url = reverse('notification_list')

    def test_get_notifications(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['verb'], 'test notification')
