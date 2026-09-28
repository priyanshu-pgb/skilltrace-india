from django.db import models
from django.conf import settings
from skills.models import Skill

class ProjectSubmission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_submissions')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='project_submissions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=250, help_text="Comma-separated technologies e.g. Django, MySQL, Bootstrap")
    github_url = models.URLField(max_length=300)
    live_demo_url = models.URLField(max_length=300, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    score = models.FloatField(default=0.0, help_text="Admin evaluated score 0-100")
    admin_feedback = models.TextField(blank=True, default='')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_projects')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.title} by {self.user.username} ({self.get_status_display()})"
