from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib import messages
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


class QuestionShowView(UpdateView):
    template_name = 'question.html'
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        q = Question.objects.get(id=post.id)
        # 回答者一覧に回答者の名前がない場合、追加
        if (q.answer_user_exists(user.username) == False):
            post.answer_user.set(q.answer_user.all())
            post.answer_user.add(user)
        # 回答が正解か判定し、
        if (q.is_correct(post.answer) == True):
            # 正解者一覧に正解者の名前がない場合、追加
            if (q.solve_user_exists(user.username) == False):
                post.solve_user.set(q.solve_user.all())
                post.solve_user.add(user)
        post.answer = q.answer
        post.save()
        return redirect('/ctf_app/')

"""
# 未完成
def vote(request):
    form = QuestionForm(request.POST)
    print(form.Meta.fields)
    username = form.Meta.fields[0]
    q = Question.objects.get(username)
    if request.method == 'POST':
        if 'good' in request.POST:
            print(good)
            q.vote_good(name=username)
        elif 'bad' in request.POST:
            print(bad)
            q.vote_bad(name=username)
"""