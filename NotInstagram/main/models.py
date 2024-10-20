from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    img = models.ImageField(upload_to = 'main',null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)