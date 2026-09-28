from django.db import models
from django.conf import settings
from skills.models import Skill, level_num_to_name

class TrainingCourse(models.Model):
    LEVEL_CHOICES = (
        (1, 'Beginner'),
        (2, 'Basic'),
        (3, 'Intermediate'),
        (4, 'Advanced'),
        (5, 'Expert'),
    )
    name = models.CharField(max_length=200)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='training_courses')
    target_level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=3)
    description = models.TextField()
    provider = models.CharField(max_length=150, default='SkillBridge Learning')
    duration = models.CharField(max_length=100, default='4 Weeks (20 Hours)')
    url = models.URLField(max_length=400, blank=True, default='https://example.com/course')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_target_level_display()})"


class TrainingEnrollment(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress_percent = models.PositiveIntegerField(default=0)
    
    # Longitudinal re-assessment impact metrics
    score_before = models.FloatField(null=True, blank=True, help_text="Skill score before enrolling")
    score_after = models.FloatField(null=True, blank=True, help_text="Skill score after completion re-assessment")
    
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name} ({self.progress_percent}%)"

    @property
    def improvement_delta(self):
        if self.score_before is not None and self.score_after is not None:
            return round(self.score_after - self.score_before, 1)
        return None
