from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import LoginForm


def index(request):
    params = {"message_me": "Hello World"}
    return render(request, 'index.html', context=params)


class UserCreateView(CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm


class UserLogoutView(LogoutView):
    template_name = 'logout.html'


