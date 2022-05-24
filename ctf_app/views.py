from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Question
from .forms import LoginForm, QuestionForm


# def index(request):
#     params = {"message_me": "Hello World"}
#     return render(request, 'index.html', context=params)
class QuestionListView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Question


class UserCreateView(CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm


class UserLogoutView(LogoutView):
    template_name = 'logout.html'


class QuestionCreateView(CreateView):
    template_name = 'new.html'
    form_class = QuestionForm
    success_url = reverse_lazy('index')


class QuestionShowView(DetailView):
    template_name = 'question.html'
    model = Question
