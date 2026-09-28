from django.contrib import admin
from .models import EmploymentRecord

@admin.register(EmploymentRecord)
class EmploymentRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'company_name', 'job_role', 'salary_range', 'is_verified_by_admin', 'updated_at')
    list_filter = ('status', 'employment_type', 'is_verified_by_admin')
    search_fields = ('user__username', 'company_name', 'job_role')
