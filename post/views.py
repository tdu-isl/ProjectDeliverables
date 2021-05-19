from post.forms import PostCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .models import Post


class IndexView(generic.ListView):
    model = Post


class DeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('accounts:profile')

    def test_func(self):
        user = self.request.user
        return user.pk == self.get_object().account.pk or user.is_superuser


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PostCreateForm
    template_name = 'post/post_create.html'

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)


def show_top(request):
    return redirect('post:home')
