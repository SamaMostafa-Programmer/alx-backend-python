# chats/urls.py
from django.urls import path, include
from rest_framework import routers  # مهم: import routers هنا
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()  # لازم يكون DefaultRouter() من routers
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('api/', include(router.urls)),
]
