from django import forms
from .models import Post
from cloudinary.forms import CloudinaryFileField


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
