from django import forms

from .models import (
    Blog,
    Note,
    NoteStatus,
)


class BlogForm(forms.Form):
    theme = forms.CharField(max_length=Blog._meta.get_field('theme').max_length)

    class Meta:
        model = Blog
        fields = ['theme', ]


class NoteForm(forms.Form):
    title = forms.CharField(
        max_length=Note._meta.get_field('title').max_length)
    body = forms.CharField(
        max_length=Note._meta.get_field('body').max_length)

    class Meta:
        model = Note
        fields = ['title', 'body']


class NoteStatusForm(forms.Form):
    status = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = NoteStatus
        fields = ['status']
