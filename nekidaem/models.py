
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from transliterate import translit


def get_email(blog_id):
    sub_list = Subscription.objects.filter(blog_id=blog_id)

    if sub_list:
        emails = [sub.subscriber.email for sub in sub_list]
    else:
        emails = []
    return emails


class Blog(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=256, default='Мой блог')
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        latin_username = translit(self.author.username, 'ru', reversed=True)
        self.slug = slugify(latin_username)
        super(Blog, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['author', 'theme']

    def __str__(self):
        return self.theme


class Note(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, default='')
    body = models.TextField(max_length=2000, default='')
    time = models.DateTimeField(blank=True)
    make_public = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('show_note', kwargs={'blog_name_slug': self.blog.slug, 'note_id': self.id})

    def send_notification(self):
        url = self.get_absolute_url()
        blog_id = self.blog.id
        emails = get_email(blog_id)

        message_context = {
            'author': self.blog.author.username,
            'url': url,
            'title': self.title
        }
        html_message = render_to_string('notification_message.html', message_context)

        subject = 'Опубликован новый пост!'
        message = strip_tags(html_message)
        send_mail(subject, message, None, emails, html_message=html_message)

    def save(self, *args, **kwargs):
        super(Note, self).save(*args, **kwargs)
        if self.make_public:
            self.send_notification()

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
