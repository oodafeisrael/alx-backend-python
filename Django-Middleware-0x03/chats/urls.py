"""
URL configuration for the chats app.
This sets up API routes using Django REST Framework's DefaultRouter.
"""

from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

# Create a defaultRouter instance using routers.DefaultRouter()
router = routers.DefaultRouter()

# Create a DefaultRouter instance
# router = DefaultRouter()

# Register the viewsets with appropriate route names
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Nested router for messages under conversations
convo_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# URL patterns using the router

all_routes = router.urls + convo_router.urls

urlpatterns = [
    path('', include(all_routes)),
]
