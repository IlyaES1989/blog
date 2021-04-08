from django.urls import path
from .views import (
    BlogView,
    CreateNote,
    SubscribeFor,
)

urlpatterns = [
    path('', BlogView.as_view(), name='index'),
    path('create/', CreateNote.as_view(), name='create'),
    path('subscribe/', SubscribeFor.as_view(), name='subscribe'),
]
