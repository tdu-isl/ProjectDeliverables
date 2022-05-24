from django.db import models
from django.contrib.auth.models import User


def file_upload_path(instance, filename):
    return f'{str(instance.user.id)}/{filename}'


class Question(models.Model):
    class Meta:
        verbose_name_plural = '問題'

    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    answer = models.CharField(max_length=100)
    link = models.SlugField(null=True, blank=True)
    upload = models.FileField(upload_to='uploads/%Y/%m', blank=True, null=True)
    answer_user = models.ManyToManyField(User, blank=True, related_name='ans_user')
    solve_user = models.ManyToManyField(User, blank=True, related_name='solve')

    def __str__(self):
        return f'{str(self.id)}: {self.title}'
