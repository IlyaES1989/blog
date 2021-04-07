
from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=256, default='My blog')

    class Meta:
        unique_together = ['author', 'theme']

    def __str__(self):
        return self.theme


class Post(models.Model):
    author = models.OneToOneField(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, default='')
    body = models.CharField(max_length=2000, default='')
    time = models.DateTimeField(blank=True)
    notification_message = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
    subscriber = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['blog', 'subscriber']


class PostStatus(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    subscriber = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
