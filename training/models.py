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


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_aspirational = models.BooleanField(default=False, help_text="NITI Aayog Aspirational District")

    class Meta:
        ordering = ['state', 'name']
        unique_together = ('name', 'state')

    def __str__(self):
        asp = " [Aspirational]" if self.is_aspirational else ""
        return f"{self.name}, {self.state}{asp}"


class TrainingProvider(models.Model):
    name = models.CharField(max_length=200)
    nsdc_partner_code = models.CharField(max_length=50, unique=True, help_text="SMART / NSDC Partner ID")
    accreditation_grade = models.CharField(max_length=10, default='A', choices=(('A+', 'A+'), ('A', 'A'), ('B', 'B'), ('C', 'C')))
    contact_person = models.CharField(max_length=100, blank=True, default='')
    contact_phone = models.CharField(max_length=20, blank=True, default='')
    contact_email = models.EmailField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.nsdc_partner_code})"


class TrainingCentre(models.Model):
    provider = models.ForeignKey(TrainingProvider, on_delete=models.CASCADE, related_name='centres')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='training_centres')
    center_name = models.CharField(max_length=200)
    center_code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.center_name} - {self.district.name}"


class Cohort(models.Model):
    SCHEME_CHOICES = (
        ('pmkvy4', 'PMKVY 4.0 (Skill India)'),
        ('ddu_gky', 'DDU-GKY (Rural Development)'),
        ('vishwakarma', 'PM-Vishwakarma Scheme'),
        ('naps', 'National Apprenticeship Promotion (NAPS)'),
        ('state_mission', 'State Skill Development Mission (SSDM)'),
        ('csr_initiative', 'Corporate CSR Skilling Program'),
    )
    batch_code = models.CharField(max_length=50, unique=True)
    scheme_name = models.CharField(max_length=50, choices=SCHEME_CHOICES, default='pmkvy4')
    training_centre = models.ForeignKey(TrainingCentre, on_delete=models.CASCADE, related_name='cohorts', null=True, blank=True)
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='cohorts')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.batch_code} ({self.get_scheme_name_display()})"


class TrainingEnrollment(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='enrollments')
    cohort = models.ForeignKey(Cohort, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')
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
