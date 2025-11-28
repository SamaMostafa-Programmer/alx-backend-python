from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from .models import Message

@cache_page(60)  # 60 seconds cache
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(receiver=request.user).select_related("sender", "parent_message").prefetch_related("replies")
    return render(request, "messages.html", {"messages": messages})
