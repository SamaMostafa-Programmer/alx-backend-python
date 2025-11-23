from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import MessageSerializer
from .permissions import IsParticipant
from .pagination import MessagePagination
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.status import HTTP_403_FORBIDDEN  # REQUIRED

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]  # REQUIRED
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter  # REQUIRED

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")  # REQUIRED
        
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Message.objects.none()

        return Message.objects.filter(conversation_id=conversation_id)  # REQUIRED

    def create(self, request, *args, **kwargs):
        conversation_id = kwargs.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not allowed in this conversation."},
                status=HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)
