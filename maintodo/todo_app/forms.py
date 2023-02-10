from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ToDoTask


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = ''
        self.fields['email'].initial = ''

class ToDoTaskForm(forms.ModelForm):
    class Meta:
        model = ToDoTask
        fields = ['title', 'description', 'complete']