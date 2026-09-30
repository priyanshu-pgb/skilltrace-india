from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('health/', views.health_check, name='health_check'),
    path('api/chat/', views.chat_assistant_api, name='chat_assistant_api'),
]
