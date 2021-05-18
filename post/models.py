from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post:home')
