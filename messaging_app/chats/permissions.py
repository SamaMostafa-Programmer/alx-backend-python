from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to authenticated users who are participants
    of the conversation linked to the message.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj may be a Conversation or a Message.
        """
        user = request.user

        # If it's a conversation object
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # If it's a message object (it must have obj.conversation)
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        return False
