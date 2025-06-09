import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_time = django_filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_time = django_filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr='lte')
    sender = django_filters.CharFilter(field_name="sender__email", lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['sender', 'start_time', 'end_time']
