from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone


from .models import (
    Blog,
    Note,
    Subscription,
)

from .forms import (
    NoteStatus,
    NoteForm,
)


def get_user(request):
    user = User.objects.get(username=request.user.username)
    return user


@method_decorator(login_required, name='dispatch')
class BlogView(View):
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

        response = render(request, self.template_name, context_dict)
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


class CreateNote(View):
    template_name = 'create_note.html'
    form_class = NoteForm

    def get(self, request):
        form = self.form_class()
        response = render(request, self.template_name, {'form': form})
        return response

    def post(self, request):
        user = get_user(request)
        author = Blog.objects.get_or_create(author=user)[0]
        print(author)
        title = request.POST.get('title')
        body = request.POST.get('body')
        time = timezone.now()

        Note.objects.create(
            author=author,
            title=title,
            body=body,
            time=time,
            notification_message=True,
        )
        return redirect('index')


class SubscribeFor(View):
    template_name = 'subscribe.html'

    def get(self, request):
        user = get_user(request)
        user_id = request.user.id
        subscriptions = Subscription.objects.filter(subscriber=user_id)
        sub_blog_id = [blog.blog.id for blog in subscriptions]

        user_blog = Blog.objects.get_or_create(author=user)[0]
        user_blog_id = [user_blog.id]

        exclude_list = sub_blog_id + user_blog_id

        try:
            other_blogs = Blog.objects.exclude(id__in=exclude_list)
        except TypeError:
            other_blogs = None

        context_dict = {
            'subscriptions': subscriptions,
            'other_blogs': other_blogs,
        }
        response = render(request, self.template_name, context_dict)
        return response

    def post(self, request):
        user_id = request.user.id
        user = get_user(request)
        blog_id = request.POST.get('blog_id')
        blog = Blog.objects.get(id=blog_id)

        try:
            unsub = Subscription.objects.get(blog_id=blog_id, subscriber_id=user_id)
            unsub.delete()
        except Subscription.DoesNotExist:
            Subscription.objects.create(blog=blog,subscriber=user)

        return redirect('subscribe')