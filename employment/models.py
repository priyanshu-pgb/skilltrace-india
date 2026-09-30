import uuid
from django.db import models
from django.conf import settings

class EmploymentRecord(models.Model):
    STATUS_CHOICES = (
        ('employed', 'Formally Employed'),
        ('unemployed', 'Seeking Employment / Unemployed'),
        ('internship', 'Active Internship / Apprenticeship (NAPS)'),
        ('freelancing', 'Freelancing / Gig Economy'),
        ('self_employed', 'Self-Employed / Micro-Entrepreneur'),
        ('higher_studies', 'Higher Education / Studies'),
        ('dropped_out', 'Inactive / Exited Labor Market'),
    )
    TYPE_CHOICES = (
        ('full_time', 'Full-time Permanent'),
        ('part_time', 'Part-time'),
        ('contract', 'Contractual / Fixed-Term'),
        ('intern', 'Apprenticeship / Intern'),
        ('freelance', 'Self-Employed / Freelance'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employment_record')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='unemployed')
    company_name = models.CharField(max_length=150, blank=True, default='')
    job_role = models.CharField(max_length=150, blank=True, default='')
    joining_date = models.DateField(null=True, blank=True)
    salary_range = models.CharField(max_length=100, blank=True, default='')
    current_monthly_wage = models.PositiveIntegerField(null=True, blank=True, help_text="Current monthly take-home salary in ₹")
    location = models.CharField(max_length=100, blank=True, default='')
    employment_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='full_time', blank=True)
    skills_used = models.CharField(max_length=300, blank=True, default='', help_text="Skills applied in current role")
    
    # Relevance of Training to Current Livelihood
    RELEVANCE_CHOICES = (
        ('high', 'Directly Relevant (Daily Application)'),
        ('partial', 'Partially Relevant (Some Concepts Used)'),
        ('low', 'Minimally Relevant'),
        ('none', 'Not Relevant At All (Different Domain)'),
    )
    training_relevance = models.CharField(max_length=20, choices=RELEVANCE_CHOICES, default='high')
    
    # Credibility & Validation Signals
    is_verified_by_admin = models.BooleanField(default=False, help_text="Whether verified via employer token or administrative audit")
    epfo_uan = models.CharField(max_length=30, blank=True, default='', help_text="Masked EPFO UAN or Social Security Signal")
    employer_gstin = models.CharField(max_length=30, blank=True, default='', help_text="Employer GSTIN")
    last_milestone_month = models.IntegerField(default=0, help_text="Latest completed milestone (0, 3, 6, 12, 24 mo)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.get_status_display()}"


class LongitudinalMilestone(models.Model):
    """
    Time-series ledger tracking job retention, wage growth, and livelihood progression
    at Month 0 (Exit), Month 3, Month 6, Month 12, and Month 24.
    """
    MILESTONE_CHOICES = (
        (0, 'Month 0 (Placement / Initial Exit)'),
        (3, 'Month 3 (Early Retention Check)'),
        (6, 'Month 6 (Mid-Term Retention Check)'),
        (12, 'Month 12 (1-Year Sustained Livelihood)'),
        (24, 'Month 24 (Long-Term Economic Mobility)'),
    )
    VERIFICATION_SOURCES = (
        ('self_reported', 'Trainee WhatsApp/SMS Quick Response'),
        ('employer_confirmed', 'Employer 1-Click Token Confirmation'),
        ('assisted_call', 'Rozgar Sahayak / Call Center Outbound'),
        ('epfo_signal', 'EPFO / Bank Remittance Signal'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='longitudinal_milestones')
    milestone_month = models.IntegerField(choices=MILESTONE_CHOICES)
    status = models.CharField(max_length=30, choices=EmploymentRecord.STATUS_CHOICES)
    company_name = models.CharField(max_length=150, blank=True, default='')
    job_role = models.CharField(max_length=150, blank=True, default='')
    monthly_wage = models.PositiveIntegerField(default=0, help_text="Actual monthly take-home in ₹")
    is_retained = models.BooleanField(default=True, help_text="Active in formal or productive livelihood")
    is_wage_increased = models.BooleanField(default=False, help_text="Wage increased compared to earlier milestone")
    training_relevance = models.CharField(max_length=20, choices=EmploymentRecord.RELEVANCE_CHOICES, default='high')
    verification_source = models.CharField(max_length=30, choices=VERIFICATION_SOURCES, default='self_reported')
    check_in_date = models.DateField()
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user', 'milestone_month']
        unique_together = ('user', 'milestone_month')

    def __str__(self):
        return f"{self.user.username} - Month {self.milestone_month}: ₹{self.monthly_wage:,}/mo ({self.get_status_display()})"


class NonPlacementReason(models.Model):
    """
    Captures systemic root causes for attrition or non-placement to inform
    curriculum redesign, counseling, and district resource allocation.
    """
    REASON_CATEGORIES = (
        ('relocation_refusal', 'Reluctance to Migrate Away from Home District'),
        ('wage_dissatisfaction', 'Offered Wage Inadequate for Urban Living Costs'),
        ('family_marriage', 'Caregiving / Family Opposition / Marriage Constraints'),
        ('skill_mismatch', 'Skill Gap / Failed Practical Employer Evaluation'),
        ('local_opportunity_lack', 'Absence of Relevant Industrial Clusters Locally'),
        ('health_personal', 'Medical or Personal Emergency'),
        ('joined_informal', 'Opted for Traditional / Unorganized Daily Wage'),
        ('higher_education', 'Enrolled in Full-Time Higher Degree'),
        ('other', 'Other Reason'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attrition_reasons')
    category = models.CharField(max_length=40, choices=REASON_CATEGORIES)
    details = models.TextField(help_text="Context shared by candidate or mobilizer")
    recommended_action = models.TextField(blank=True, default='', help_text="Suggested intervention (e.g. Local apprenticeship, stipend, relocation grant)")
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.get_category_display()}"


class FollowUpLog(models.Model):
    """
    Tracks multi-channel automated and assisted follow-up outreach
    to overcome phone number changes and location migration.
    """
    CHANNEL_CHOICES = (
        ('whatsapp_bot', 'Automated WhatsApp Conversational Bot'),
        ('ivr_voice', 'Automated Interactive Voice Response (IVR)'),
        ('sms_link', 'Tokenized 1-Click SMS Link'),
        ('assisted_call', 'Rozgar Sahayak (Tele-Calling Mobilizer)'),
        ('field_visit', 'Physical Centre / Field Mobilizer Visit'),
    )
    CONTACT_TYPE_CHOICES = (
        ('primary', 'Primary Mobile'),
        ('alt', 'Alternative Mobile'),
        ('guardian', 'Guardian / Village Relative Contact'),
    )
    STATUS_CHOICES = (
        ('pending', 'Queued for Dispatch'),
        ('delivered', 'Delivered / Awaiting Response'),
        ('responded', 'Response Received'),
        ('unreachable', 'Switched Off / Out of Coverage'),
        ('wrong_number', 'Wrong Number / SIM Changed'),
        ('escalated', 'Escalated to Alternative Contact'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followup_logs')
    channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES)
    contact_number_used = models.CharField(max_length=20)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, default='primary')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='delivered')
    response_text = models.TextField(blank=True, default='')
    logged_at = models.DateTimeField(auto_now_add=True)
    scheduled_next_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_channel_display()} ({self.get_status_display()})"


class EmployerVerificationRequest(models.Model):
    """
    Low-burden tokenized verification link for employers to confirm placement,
    designation, wage, and retention without creating a full user account.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending Employer Review'),
        ('confirmed', 'Verified & Confirmed'),
        ('disputed', 'Disputed by Employer'),
        ('expired', 'Link Expired'),
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_verifications')
    company_name = models.CharField(max_length=150)
    employer_contact_name = models.CharField(max_length=150, blank=True, default='')
    employer_email = models.EmailField(blank=True, default='')
    employer_phone = models.CharField(max_length=20, blank=True, default='')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confirmed_role = models.CharField(max_length=150, blank=True, default='')
    confirmed_monthly_wage = models.PositiveIntegerField(null=True, blank=True)
    confirmed_joining_date = models.DateField(null=True, blank=True)
    gstin = models.CharField(max_length=30, blank=True, default='', help_text="Employer GSTIN")
    has_epfo_coverage = models.BooleanField(default=False, help_text="Candidate covered under EPFO/ESIC")
    feedback_on_trainee = models.TextField(blank=True, default='', help_text="Manager feedback on skill readiness")
    
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Verify {self.user.username} @ {self.company_name} [{self.get_status_display()}]"
