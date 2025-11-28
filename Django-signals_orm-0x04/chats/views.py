# chats/views.py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @method_decorator(cache_page(60))  # cache for 60 seconds
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
