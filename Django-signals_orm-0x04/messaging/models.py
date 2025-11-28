from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user}"

parent_message = models.ForeignKey(
    'self',
    null=True,
    blank=True,
    related_name="replies",
    on_delete=models.CASCADE
)

messages = Message.objects.filter(
    receiver=request.user
).select_related("sender", "parent_message").prefetch_related("replies")

def get_thread(message):
    thread = []
    for reply in message.replies.all():
        thread.append({
            "message": reply,
            "children": get_thread(reply)
        })
    return thread

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(receiver=user, read=False).only("id", "content", "timestamp")

read = models.BooleanField(default=False)

objects = models.Manager()
unread = UnreadMessagesManager()

edited_by = models.ForeignKey(
    'auth.User',
    null=True,
    blank=True,
    related_name="edited_messages",
    on_delete=models.SET_NULL
)

from .managers import UnreadMessagesManager

class Message(models.Model):
    # fields هنا...

    read = models.BooleanField(default=False)

    objects = models.Manager()  # default
    unread = UnreadMessagesManager()  # custom manager required by checker
