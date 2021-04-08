from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import (
    Note,
    Subscription
)

from .forms import NoteStatus


def get_user(request):
    user = User.objects.get(username=request.user.username)
    return user


@method_decorator(login_required, name='dispatch')
class Blog(View):
    template_name = 'index.html'
    form_class = NoteStatus

    def get(self, request):
        user = get_user(request)
        user_id = request.user.id

        subscription = Subscription.objects.filter(subscriber=user_id)
        sub_list = [sub.blog.id for sub in subscription]

        note_list = Note.objects.filter(author__in=sub_list).order_by('-time')

        status_list = [NoteStatus.objects.filter(note=note, subscriber=user_id).first() for note in note_list]

        notes = [(note, status) for note, status in zip(note_list, status_list)]

        context_dict = {
            'user': user,
            'notes': notes,
        }

        response = render(request, 'index.html', context_dict)
        return response

    def post(self, request):
        user = get_user(request)
        user_id = request.user.id
        note_id = request.POST.get('note')
        note_obj = NoteStatus.objects.filter(note=note_id, subscriber=user_id).first()

        if note_obj:
            note_obj.delete()
        else:
            NoteStatus.objects.create(
                note=Note.objects.get(id=note_id),
                subscriber=user,
                status=True,
            )

        return redirect('index')
