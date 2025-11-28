from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@cache_page(60)
def conversation_messages(request, conv_id):
    messages = Message.objects.filter(conversation_id=conv_id)
    return render(request, "messages.html", {"messages": messages})
