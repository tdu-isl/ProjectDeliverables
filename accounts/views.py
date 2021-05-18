from django.contrib.auth import get_user_model
from django.shortcuts import render
from post.models import Post


def user_profile(request, username):
    user = get_user_model().objects.get(username=username)
    context = {
        'User': user,
        'Posts': Post.objects.filter(account=user),
    }
    return render(request, 'accounts/user_profile.html', context)
