from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permission:
    - Only authenticated users
    - Only participants of a conversation can access/view/update/delete messages
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If object is a Conversation
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # If object is a Message (must check its conversation)
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        return False
