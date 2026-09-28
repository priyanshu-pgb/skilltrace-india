from django.urls import path
from . import views

urlpatterns = [
    path('', views.assessment_catalog, name='assessment_catalog'),
    path('start/<int:skill_id>/', views.start_assessment, name='start_assessment'),
    path('take/<int:attempt_id>/', views.take_assessment, name='take_assessment'),
    path('submit/<int:attempt_id>/', views.submit_assessment, name='submit_assessment'),
    path('result/<int:attempt_id>/', views.assessment_result, name='assessment_result'),
    path('practical/<int:task_id>/', views.practical_workspace, name='practical_workspace'),
    path('practical/<int:task_id>/submit/', views.submit_practical, name='submit_practical'),
]
