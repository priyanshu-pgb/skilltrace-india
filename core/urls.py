from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('health/', views.health_check, name='health_check'),
]
