from django.shortcuts import redirect
from django.contrib.auth.models import User

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect("/")
