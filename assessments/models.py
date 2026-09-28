from django.db import models
from django.conf import settings
from skills.models import Skill

class Question(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    OPTION_CHOICES = (
        ('a', 'Option A'),
        ('b', 'Option B'),
        ('c', 'Option C'),
        ('d', 'Option D'),
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="The question stem")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    option_a = models.CharField(max_length=400)
    option_b = models.CharField(max_length=400)
    option_c = models.CharField(max_length=400)
    option_d = models.CharField(max_length=400)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES, help_text="Server-side validated only")
    explanation = models.TextField(blank=True, default='', help_text="Explanation revealed after submission")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.skill.name} - {self.difficulty.upper()}] {self.text[:60]}..."


class AssessmentAttempt(models.Model):
    ATTEMPT_TYPE_CHOICES = (
        ('mcq', 'Standard MCQ Assessment'),
        ('reassessment', 'Post-Training Re-Assessment'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessment_attempts')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='assessment_attempts')
    attempt_type = models.CharField(max_length=20, choices=ATTEMPT_TYPE_CHOICES, default='mcq')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_questions = models.PositiveIntegerField(default=10)
    correct_answers = models.PositiveIntegerField(default=0)
    score_percent = models.FloatField(default=0.0)
    is_completed = models.BooleanField(default=False)
    duration_seconds = models.PositiveIntegerField(default=600) # 10 minutes limit

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        status = f"{self.score_percent}%" if self.is_completed else "In Progress"
        return f"{self.user.username} - {self.skill.name} ({self.attempt_type}): {status}"


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(AssessmentAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('attempt', 'question')


class PracticalTask(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='practical_tasks')
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    description = models.TextField()
    requirements = models.TextField(help_text="Detailed task criteria and constraints")
    starter_code = models.TextField(blank=True, default='')
    test_cases_count = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.skill.name} Practical: {self.title}"


class PracticalSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='practical_submissions')
    task = models.ForeignKey(PracticalTask, on_delete=models.CASCADE, related_name='submissions')
    submitted_code = models.TextField()
    test_cases_passed = models.PositiveIntegerField(default=0)
    total_test_cases = models.PositiveIntegerField(default=5)
    score_percent = models.FloatField(default=0.0)
    feedback = models.TextField(blank=True, default='')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} - {self.task.title}: {self.score_percent}%"
