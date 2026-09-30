from django.urls import path
from . import views

urlpatterns = [
    path('', views.skills_dashboard, name='skills_dashboard'),
    path('list/', views.skills_dashboard, name='skills_list'),
    path('claim/', views.claim_skill, name='claim_skill'),
]
