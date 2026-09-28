from django.db import models
from django.conf import settings

class EmploymentRecord(models.Model):
    STATUS_CHOICES = (
        ('employed', 'Formally Employed'),
        ('unemployed', 'Seeking Employment / Unemployed'),
        ('internship', 'Active Internship'),
        ('freelancing', 'Freelancing / Gig Economy'),
        ('self_employed', 'Self-Employed / Entrepreneur'),
        ('higher_studies', 'Higher Education / Studies'),
    )
    TYPE_CHOICES = (
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contractual'),
        ('intern', 'Internship'),
        ('freelance', 'Freelance'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employment_record')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='unemployed')
    company_name = models.CharField(max_length=150, blank=True, default='')
    job_role = models.CharField(max_length=150, blank=True, default='')
    joining_date = models.DateField(null=True, blank=True)
    salary_range = models.CharField(max_length=100, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    employment_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='full_time', blank=True)
    skills_used = models.CharField(max_length=300, blank=True, default='', help_text="Skills applied in current role")
    is_verified_by_admin = models.BooleanField(default=False, help_text="Whether employment status was verified via offer letter or audit")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.get_status_display()}"
