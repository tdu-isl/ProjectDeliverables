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
    hint = models.TextField(null=True, blank=True)
    field = models.CharField(max_length=50, null=True, blank=True)
    voted_good_user = models.ManyToManyField(User, blank=True, related_name='voted_good')
    voted_bad_user = models.ManyToManyField(User, blank=True, related_name='voted_bad')

    def __str__(self):
        return f'{str(self.id)}: {self.title}'

    # 未完成
    def is_correct(self, input_answer):
        if (input_answer==self.answer):
            return True
        return False

    # 未完成
    def answered(self, name):
        u = User.Objects.get(username=name)
        self.answer_user.add(u)

    # 未完成
    def solved(self, name):
        u = User.Objects.get(username=name)
        self.solve_user.add(u)

    def get_answer_user_num(self):
        return self.answer_user.all().count()

    def get_solve_user_num(self):
        return self.solve_user.all().count()

    # 正答率を小数第一位の%表記で返す
    def get_correct_answer_rate(self):
        a = self.answer_user.all().count()
        s = self.solve_user.all().count()
        if (a == 0):
            return 0
        result = round(s / a * 100, 1)
        return result

    # 未完成
    def vote_good(self, name):
        u = User.Objects.get(username=name)
        self.voted_good_user.add(u)

    # 未完成
    def vote_bad(self, name):
        u = User.Objects.get(username=name)
        self.voted_bad_user.add(u)

