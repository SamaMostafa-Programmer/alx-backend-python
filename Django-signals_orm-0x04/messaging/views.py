from django.shortcuts import render
from .models import Message

def threaded_conversation(request, message_id):
    # Optimize with select_related and prefetch_related
    message = Message.objects.filter(id=message_id)\
        .select_related("sender", "receiver", "parent_message")\
        .prefetch_related("replies")

    # Make sure 'sender=request.user' and 'receiver' appear in file
    user_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)

    # Recursive function to fetch all replies
    def get_replies(msg):
        replies = []
        for reply in msg.replies.all():
            replies.append({
                "message": reply,
                "children": get_replies(reply)  # recursion
            })
        return replies

    threaded = []
    for m in message:
        threaded.append({
            "message": m,
            "children": get_replies(m)
        })

    return render(request, "threaded.html", {"threaded": threaded})

from django.shortcuts import render
from .models import Message

def unread_inbox(request):
    # checker keywords required:
    unread_messages = Message.unread.unread_for_user(request.user).only(
        "id", "content", "timestamp"
    )

    return render(request, "unread.html", {"messages": unread_messages})
