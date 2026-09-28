from django.urls import path
from . import views

urlpatterns = [
    path('', views.employment_tracker, name='employment_tracker'),
]
