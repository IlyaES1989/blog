
from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=256, default='Мой блог')

    class Meta:
        unique_together = ['author', 'theme']

    def __str__(self):
        return self.theme


class Note(models.Model):
    author = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, default='')
    body = models.TextField(max_length=2000, default='')
    time = models.DateTimeField(blank=True)
    notification_message = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['blog', 'subscriber']


class NoteStatus(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        unique_together = ['note', 'subscriber']
