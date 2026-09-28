from django.contrib import admin
from .models import TrainingCourse, TrainingEnrollment

@admin.register(TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'skill', 'target_level', 'provider', 'duration')
    list_filter = ('skill', 'target_level', 'provider')
    search_fields = ('name', 'description')

@admin.register(TrainingEnrollment)
class TrainingEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'progress_percent', 'score_before', 'score_after', 'enrolled_at')
    list_filter = ('status', 'course__skill')
