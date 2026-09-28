from django.contrib import admin
from .models import ProjectSubmission

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'skill', 'status', 'score', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'skill')
    search_fields = ('title', 'user__username', 'description', 'technologies')
