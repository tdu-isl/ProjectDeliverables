from django import forms
from django.contrib.auth.forms import AuthenticationForm
from . models import Question


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('answer',)
        labels = {
            'answer': 'フラグ',
        }
