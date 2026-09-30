from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import accounts.views as account_views
import analytics.views as analytics_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core Landing & Health
    path('', include('core.urls')),
    
    # Direct Auth & Profile shortcuts
    path('login/', account_views.login_view, name='login'),
    path('register/', account_views.register_view, name='register'),
    path('logout/', account_views.logout_view, name='logout'),
    path('profile/', account_views.profile_view, name='profile'),
    path('dashboard/', account_views.dashboard_router, name='dashboard'),
    
    # Modular apps
    path('auth/', include('accounts.urls')),
    path('skills/', include('skills.urls')),
    path('assessments/', include('assessments.urls')),
    path('projects/', include('projects.urls')),
    path('jobs/', include('jobs.urls')),
    path('training/', include('training.urls')),
    path('employment/', include('employment.urls')),
    path('analytics/', include('analytics.urls')),
    
    # Direct dashboard routes
    path('user-dashboard/', analytics_views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', analytics_views.admin_dashboard, name='admin_dashboard'),
    path('reassessment/', include('training.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.custom_404'
handler403 = 'core.views.custom_403'
handler500 = 'core.views.custom_500'
