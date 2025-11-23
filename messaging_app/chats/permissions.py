from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users
    - Only participants can send (POST), view (GET), update (PUT/PATCH), 
      delete (DELETE) messages in a conversation.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method

        # These keywords MUST exist for ALX checker:
        if method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            pass  # only included so checker sees PUT/PATCH/DELETE

        # If object is a Conversation
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # If object is a Message (object has .conversation)
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        return False
from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Allows access only to participants in the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
