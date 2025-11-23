import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name="sender__id")
    date_after = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    date_before = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["user", "date_after", "date_before"]
