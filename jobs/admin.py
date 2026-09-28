from django.contrib import admin
from .models import Job, JobRequirement

class JobRequirementInline(admin.TabularInline):
    model = JobRequirement
    extra = 1

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'experience_level', 'salary_range', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [JobRequirementInline]

@admin.register(JobRequirement)
class JobRequirementAdmin(admin.ModelAdmin):
    list_display = ('job', 'skill', 'required_level', 'is_mandatory')
    list_filter = ('job', 'skill', 'required_level')
