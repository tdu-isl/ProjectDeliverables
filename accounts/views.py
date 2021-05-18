from django.contrib.auth import get_user_model
from django.shortcuts import render

def user_profile(request, username):
    context = {
        'User': get_user_model().objects.get(username=username),
    }
    return render(request, 'accounts/user_profile.html', context)