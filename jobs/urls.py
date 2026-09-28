from django.urls import path
from . import views

urlpatterns = [
    path('', views.jobs_list, name='jobs_list'),
    path('<int:job_id>/gap-report/', views.job_skill_gap_report, name='job_skill_gap_report'),
]
