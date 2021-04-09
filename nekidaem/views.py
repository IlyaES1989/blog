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

        note_list = Note.objects.filter(blog__in=sub_list).order_by('-time')

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
        blog = Blog.objects.get_or_create(author=user)[0]
        title = request.POST.get('title')
        body = request.POST.get('body')
        time = timezone.now()

        Note.objects.create(
            blog=blog,
            title=title,
            body=body,
            time=time,
            make_public=True,
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
            subscription = Subscription.objects.get(blog_id=blog_id,
                                                    subscriber_id=user_id)
            subscription.delete()
        except Subscription.DoesNotExist:
            Subscription.objects.create(blog=blog, subscriber=user)

        return redirect('subscribe')


class ShowBlog(View):
    template_name = 'blog.html'

    def get(self, request, blog_name_slug):
        try:
            blog = Blog.objects.get(slug=blog_name_slug)
            notes = Note.objects.filter(blog=blog)

            context_dict = {
                'blog': blog,
                'notes': notes,
            }
        except Blog.DoesNotExist:
            context_dict = {
                'blog': None,
                'notes': None,
            }
        return render(request, self.template_name, context_dict)


class ShowNote(View):
    template_name = 'note.html'

    def get(self, request, blog_name_slug, note_id):
        user_id = request.user.id
        note = Note.objects.get(id=note_id)
        note_status = NoteStatus.objects.filter(note=note_id,
                                                subscriber=user_id).first()

        context_dict = {
            'note': note,
            'note_status': note_status,
            'blog_name_slug': blog_name_slug,
        }
        return render(request, self.template_name, context_dict)

    def post(self, request, blog_name_slug, note_id):
        user = get_user(request)
        user_id = request.user.id
        note = Note.objects.get(id=note_id)
        note_status = NoteStatus.objects.filter(note=note_id,
                                                subscriber=user_id).first()

        if note_status:
            note_status.delete()
        else:
            NoteStatus.objects.create(
                note=Note.objects.get(id=note_id),
                subscriber=user,
                status=True,
            )
        context_dict = {
            'note': note,
            'note_status': note_status,
            'blog_name_slug': blog_name_slug,
        }
        return redirect('show_note', blog_name_slug=blog_name_slug, note_id=note_id)

