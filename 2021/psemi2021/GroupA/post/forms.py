from django import forms
from django.forms import widgets
from .models import Post, Reply
from cloudinary.forms import CloudinaryFileField


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('text',)

        labels = {
            'text': 'Reply',
        }

        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
        }
