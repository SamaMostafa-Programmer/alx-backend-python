# chats/filters.py
import django_filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # Filter messages by a participant id or username (messages from conversations that include a user)
    participant = django_filters.BaseInFilter(field_name='conversation__participants__id', lookup_expr='exact')
    participant_username = django_filters.CharFilter(field_name='conversation__participants__username', lookup_expr='iexact')

    # created_at range (expects ISO datetimes or dates): ?created_after=YYYY-MM-DD&created_before=YYYY-MM-DD
    created_after = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['participant', 'participant_username', 'created_after', 'created_before']
