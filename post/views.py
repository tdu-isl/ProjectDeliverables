from post.forms import PostCreateForm, ReplyCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from .models import Post, Reply


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


def show_detail(request, pk):
    context = {
        'post': Post.objects.get(pk=pk),
        'replies': Reply.objects.filter(target=pk),
        'form': ReplyCreateForm(),
    }
    return render(request, 'post/post_detail.html', context)


@require_POST
def create_reply(request, pk):
    form = ReplyCreateForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.target = get_object_or_404(Post, pk=pk)
        reply.account = request.user
        reply.save()
        return redirect('post:detail', pk=pk)

    context = {
        'post': Post.objects.get(pk=pk),
        'form': form,
    }
    return render(request, 'post/post_detail.html', context)


def show_top(request):
    return redirect('post:home')


def plus_post_like(request, pk):
    post = Post.objects.get(pk=pk)
    post.like += 1
    post.save()

    return redirect("post:home")
