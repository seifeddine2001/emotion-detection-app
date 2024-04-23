from django.urls import path
from . import views

urlpatterns = [
    path('', views.realtime_analyze_emotion, name='realtime_analyze_emotion'),
    path('video_feed/', views.video_feed, name='video_feed'),
    
]
