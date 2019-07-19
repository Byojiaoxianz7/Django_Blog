from django.urls import path
from .views import post_comment

urlpatterns = [
    path('post_comment', post_comment, name='post_comment'),
]

