from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('submit/', views.submit_project, name='submit_project'),
    path('review/<int:project_id>/', views.review_project, name='review_project'),
]
