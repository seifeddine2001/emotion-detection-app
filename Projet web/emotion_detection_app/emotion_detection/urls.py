

from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyze_emotion, name='analyze_emotion'),
    path('result/', views.show_result, name='result'),
]
