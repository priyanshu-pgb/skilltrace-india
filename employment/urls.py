from django.urls import path
from . import views

urlpatterns = [
    path('', views.employment_tracker, name='employment_tracker'),
    path('milestone/add/', views.record_milestone, name='record_milestone'),
    path('attrition/report/', views.record_non_placement, name='record_non_placement'),
    path('employer/request/', views.request_employer_verification, name='request_employer_verification'),
    path('verify/<uuid:token>/', views.public_employer_verify, name='public_employer_verify'),
    path('quick-checkin/', views.quick_checkin_simulate, name='quick_checkin_simulate'),
    path('outreach-console/', views.admin_outreach_console, name='admin_outreach_console'),
    path('admin-outreach/', views.admin_outreach_console, name='admin_outreach_console_alt'),
]
