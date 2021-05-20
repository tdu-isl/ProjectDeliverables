from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post:home')


class Reply(models.Model):
    text = models.TextField()
    target = models.ForeignKey(Post, on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
