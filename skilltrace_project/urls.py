from django.contrib import admin
from django.urls import path
from skilltrace import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web Pages
    path('', views.index_view, name='index'),
    path('verify/<uuid:token>/', views.employer_verify_page, name='employer_verify_page'),
    path('terms-of-service/', views.legal_tos_view, name='terms_of_service'),
    path('privacy-policy/', views.legal_privacy_view, name='privacy_policy'),

    # REST API v1
    path('api/v1/metadata/', views.MetadataView.as_view(), name='api_metadata'),
    path('api/v1/analytics/funnel/', views.AnalyticsFunnelView.as_view(), name='api_analytics_funnel'),
    path('api/v1/trainees/', views.TraineeListView.as_view(), name='api_trainees'),
    path('api/v1/identity/review-queue/', views.IdentityReviewQueueView.as_view(), name='api_identity_review'),
    path('api/v1/consent/ledger/', views.ConsentLedgerView.as_view(), name='api_consent_ledger'),
    path('api/v1/followup/workbench/', views.FollowUpWorkbenchView.as_view(), name='api_followup_workbench'),
    path('api/v1/verify/<uuid:token>/', views.EmployerVerificationView.as_view(), name='api_employer_verify'),
    path('api/v1/alerts/cases/', views.ActionCasesView.as_view(), name='api_alerts_cases'),
    path('api/v1/ingest/upload/', views.IngestionUploadView.as_view(), name='api_ingest_upload'),
    path('api/v1/audit/logs/', views.AuditTrailView.as_view(), name='api_audit_logs'),
    path('api/v1/policy/overview/', views.PolicyOverviewView.as_view(), name='api_policy_overview'),
    path('api/v1/trainee/checkin/', views.TraineeCheckinView.as_view(), name='api_trainee_checkin'),
    path('api/v1/admin/grievances/', views.GrievanceQueueView.as_view(), name='api_admin_grievances'),
    path('api/v1/admin/taxonomy/', views.TaxonomyRulesView.as_view(), name='api_admin_taxonomy'),
]

