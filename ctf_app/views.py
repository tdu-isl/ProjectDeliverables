from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Question
from .forms import LoginForm, QuestionForm


class QuestionListView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Question

    def get_context_data(self, **kwargs):
        name = self.request.user.username
        context = super().get_context_data(**kwargs)
        context['has_solved_list'] = {}
        for id in range(Question.objects.all().count()):
            question = Question.objects.get(id=id+1)
            context['has_solved_list'][id+1] = question.solve_user_exists(name)
        return context


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
        user = self.request.user
        post = form.save(commit=False)
        q = Question.objects.get(id=post.id)
        if 'answer' in self.request.POST:
            # 回答者一覧に回答者の名前がない場合、追加
            if not q.answer_user_exists(user.username):
                post.answer_user.set(q.answer_user.all())
                post.answer_user.add(user)
            # 回答が正解か判定し、
            if q.is_correct(post.answer):
                messages.info(self.request, '正解')
                # 正解者一覧に正解者の名前がない場合、追加
                if not q.solve_user_exists(user.username):
                    post.solve_user.set(q.solve_user.all())
                    post.solve_user.add(user)
            if not q.is_correct(post.answer):
                messages.info(self.request, '不正解')
            post.answer = q.answer
            post.save()
        #return HttpResponseRedirect('/ctf_app/')
        return HttpResponseRedirect('/ctf_app/'+str(q.id))
