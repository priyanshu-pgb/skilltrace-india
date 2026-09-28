from django.contrib import admin
from .models import Question, AssessmentAttempt, AttemptAnswer, PracticalTask, PracticalSubmission

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'skill', 'difficulty', 'correct_option')
    list_filter = ('skill', 'difficulty', 'correct_option')
    search_fields = ('text', 'explanation')

    def text_preview(self, obj):
        return obj.text[:75]
    text_preview.short_description = 'Question'

@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'attempt_type', 'score_percent', 'is_completed', 'started_at')
    list_filter = ('attempt_type', 'is_completed', 'skill')
    search_fields = ('user__username', 'skill__name')

@admin.register(PracticalTask)
class PracticalTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'skill', 'difficulty', 'test_cases_count')
    list_filter = ('skill', 'difficulty')

@admin.register(PracticalSubmission)
class PracticalSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'test_cases_passed', 'total_test_cases', 'score_percent', 'submitted_at')
    list_filter = ('task__skill',)
