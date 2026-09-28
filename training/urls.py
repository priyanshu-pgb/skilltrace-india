from django.urls import path
from . import views

urlpatterns = [
    path('', views.training_catalog, name='training_catalog'),
    path('my-courses/', views.my_training, name='my_training'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('progress/<int:enrollment_id>/', views.update_progress, name='update_progress'),
    path('reassessment/', views.reassessment_overview, name='reassessment_overview'),
]
