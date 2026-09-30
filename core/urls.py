from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('health/', views.health_check, name='health_check'),
    path('api/chat/', views.chat_assistant_api, name='chat_assistant_api'),
    
    # Legal & Compliance Pages (DPDP Act 2023 & IT Act 2000)
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('privacy/', views.privacy_policy),
    path('terms-and-conditions/', views.terms_conditions, name='terms_conditions'),
    path('terms/', views.terms_conditions),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('cookies/', views.cookie_policy),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('grievance-redressal/', views.grievance_redressal, name='grievance_redressal'),
    path('grievance/', views.grievance_redressal),
]
