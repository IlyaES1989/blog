from django.urls import path
from .views import (
    BlogView,
    CreateNote,
    SubscribeFor,
    ShowBlog,
    ShowNote,
)
from . import views


urlpatterns = [
    path('', BlogView.as_view(), name='index'),
    path('create/', CreateNote.as_view(), name='create'),
    path('subscribe/', SubscribeFor.as_view(), name='subscribe'),
    path('subscribe/<slug:blog_name_slug>/', ShowBlog.as_view(), name='show_blog'),
    path('subscribe/<slug:blog_name_slug>/<int:note_id>', ShowNote.as_view(), name='show_note'),
]
