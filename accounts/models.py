from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Student / Candidate'),
        ('admin', 'System Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # National Skilling / SIDH Unique Trainee Registry
    trainee_id = models.CharField(max_length=50, blank=True, default='', help_text="Skill India Digital (SIDH) / APAAR Identifier")
    alt_phone = models.CharField(max_length=20, blank=True, default='', help_text="Secondary/Alternative phone to prevent contact drift")
    guardian_phone = models.CharField(max_length=20, blank=True, default='', help_text="Family/Village contact for assisted outreach")
    
    # Demographics for national equity analysis
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('transgender', 'Transgender'),
        ('undisclosed', 'Prefer not to say'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='undisclosed')
    
    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('obc', 'OBC'),
        ('sc', 'SC'),
        ('st', 'ST'),
        ('ews', 'EWS'),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    
    AREA_CHOICES = (
        ('rural', 'Rural'),
        ('semi_urban', 'Semi-Urban'),
        ('urban', 'Urban'),
    )
    area_type = models.CharField(max_length=20, choices=AREA_CHOICES, default='urban')
    is_pwd = models.BooleanField(default=False, help_text="Person with Disability (Divyangjan)")
    
    # DPDP Act 2023 Consent Architecture
    consent_given = models.BooleanField(default=True, help_text="Consent for longitudinal livelihood tracking")
    consent_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    allow_whatsapp_outreach = models.BooleanField(default=True, help_text="Permission for automated WhatsApp milestone pings")

    @property
    def is_admin_role(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_student_role(self):
        return self.role == 'user'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    degree = models.CharField(max_length=150, blank=True, default='')
    institution = models.CharField(max_length=200, blank=True, default='')
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    experience_summary = models.TextField(blank=True, default='')
    target_role = models.CharField(max_length=150, blank=True, default='Software Engineer')
    headline = models.CharField(max_length=200, blank=True, default='')
    linkedin_url = models.URLField(max_length=300, blank=True, default='')
    github_url = models.URLField(max_length=300, blank=True, default='')
    portfolio_url = models.URLField(max_length=300, blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
