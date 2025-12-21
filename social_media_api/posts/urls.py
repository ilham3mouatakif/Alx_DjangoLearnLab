from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'feed', FeedView, basename='feed')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view({'get': 'list'}), name='feed'),
]
