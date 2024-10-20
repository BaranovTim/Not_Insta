from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'img']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
