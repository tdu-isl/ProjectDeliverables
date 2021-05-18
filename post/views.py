from post.forms import PostCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from .models import Post


class IndexView(generic.ListView):
    model = Post


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PostCreateForm
    template_name = 'post/post_create.html'

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)


def show_top(request):
    return redirect('post:home')
