from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages


class Question(models.Model):
    class Meta:
        verbose_name_plural = '問題'
    
    def file_upload_path(instance, filename):
        return f'uploads/{instance.id}/{filename}'

    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    answer = models.TextField()
    link = models.SlugField(null=True, blank=True)
    upload = models.FileField(upload_to='file/%Y/%m/%d', blank=True, null=True)
    answer_user = models.ManyToManyField(User, blank=True, related_name='ans_user')
    solve_user = models.ManyToManyField(User, blank=True, related_name='solve')
    hint = models.TextField(null=True, blank=True)
    field = models.CharField(max_length=50, null=True, blank=True)
    voted_good_user = models.ManyToManyField(User, blank=True, related_name='voted_good')
    voted_bad_user = models.ManyToManyField(User, blank=True, related_name='voted_bad')

    def __str__(self):
        return f'{str(self.id)}: {self.title}'

    def is_correct(self, input_answer):
        if input_answer == self.answer:
            return True
        return False

    def answer_user_exists(self, name):
        if self.answer_user.filter(username=name).exists():
            return True
        return False

    def solve_user_exists(self, name):
        if self.solve_user.filter(username=name).exists():
            return True
        return False

    def get_answer_user_num(self):
        return self.answer_user.all().count()

    def get_solve_user_num(self):
        return self.solve_user.all().count()

    # 正答率を小数第一位の%表記で返す
    def get_correct_answer_rate(self):
        a = self.answer_user.all().count()
        s = self.solve_user.all().count()
        if a == 0:
            return 0
        result = round(s / a * 100, 1)
        return result

    def can_vote(self, name):
        if self.voted_good_user.filter(username=name).exists() or self.voted_bad_user.filter(username=name).exists():
            return False
        return True

    def get_voted_good_user_num(self):
        return self.voted_good_user.all().count()

    def get_voted_bad_user_num(self):
        return self.voted_bad_user.all().count()

    
    # def save(self, *args, **kwargs):
    #     if self.id is None:
    #         uploaded_file = self.file

    #         self.file = None
    #         super().save(*args, **kwargs)

    #         self.file = uploaded_file
    #         if "force_insert" in kwargs:
    #             kwargs.pop("force_insert")
    
    #     super().save(*args, **kwargs)

    