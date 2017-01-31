from django.conf.urls import url
from . import views
from .youtube_sdk.youtube import youtube_video
from .twitter.search import tweet
from .AUTH.Linkedin import call, callback

urlpatterns = [
    url(r'^call/', views.call,name="call"),
    url(r'^tweet/', tweet, name="tweet"),
    url(r'^youtube', youtube_video, name="youtube"),
    url(r'^auth', call),
    url(r'^callback', callback)
]