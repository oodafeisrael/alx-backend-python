"""
URL configuration for the chats app.
This sets up API routes using Django REST Framework's DefaultRouter.
"""

from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create a defaultRouter instance using routers.DefaultRouter()
router = routers.DefaultRouter()

# Create a DefaultRouter instance
router = DefaultRouter()

# Register the viewsets with appropriate route names
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# URL patterns using the router
urlpatterns = [
    path('', include(router.urls)),
]
