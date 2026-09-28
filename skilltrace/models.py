import uuid
import hashlib
from django.db import models


class State(models.Model):
    code = models.CharField(max_length=2, primary_key=True)  # LGD 2-digit e.g. '27'
    name = models.CharField(max_length=100)
    min_wage_monthly = models.IntegerField(default=14500)  # INR per month

    def __str__(self):
        return f"{self.code} - {self.name}"


class District(models.Model):
    code = models.CharField(max_length=6, primary_key=True)  # LGD district code
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    labour_market_index = models.FloatField(default=0.75)  # 0.0 to 1.0

    def __str__(self):
        return f"{self.name} ({self.state.code})"


class Scheme(models.Model):
    code = models.CharField(max_length=20, primary_key=True)  # PMKVY, DDU_GKY, NAPS, ITI_CTS, MSSDS
    name = models.CharField(max_length=200)
    central_ministry = models.CharField(max_length=100)  # MSDE, MoRD, DGT

    def __str__(self):
        return self.name


class Course(models.Model):
    course_code = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=255)
    sector = models.CharField(max_length=100)  # Automotive, Electronics, Healthcare, etc.
    nsqf_level = models.IntegerField(default=4)
    nco_code = models.CharField(max_length=20)  # NCO 2015 code
    duration_hours = models.IntegerField(default=300)

    def __str__(self):
        return f"{self.course_code}: {self.title} (NSQF {self.nsqf_level})"


class Provider(models.Model):
    code = models.CharField(max_length=30, primary_key=True)  # TC ID e.g. TC-MH-0192
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    address = models.TextField()
    accreditation_grade = models.CharField(max_length=10, default="A")  # A++, A, B, C
    geo_lat = models.FloatField(default=19.0760)
    geo_lng = models.FloatField(default=72.8777)
    risk_score = models.FloatField(default=0.08)  # Anomaly/risk index

    def __str__(self):
        return f"{self.code} - {self.name}"


class Person(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("MERGED", "Merged"),
        ("FLAGGED", "Flagged"),
        ("ARCHIVED", "Archived"),
    ]
    stid = models.CharField(max_length=20, primary_key=True, editable=False)  # ST-XX-XXXXXXXX
    state_code_first = models.CharField(max_length=2, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    merged_into = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="merged_records")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stid


class PersonPII(models.Model):
    """
    Simulated Identity Vault Table (separated from analytics/aggregates).
    Stores encrypted/tokenized demographic identity.
    """
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="pii")
    full_name = models.CharField(max_length=200)
    dob = models.DateField()
    gender = models.CharField(max_length=20, choices=[("MALE", "Male"), ("FEMALE", "Female"), ("TRANSGENDER", "Transgender")])
    guardian_name = models.CharField(max_length=200, blank=True)
    address_line = models.TextField()
    phone_hash = models.CharField(max_length=64, db_index=True)  # HMAC-SHA256
    phone_last4 = models.CharField(max_length=4)
    category = models.CharField(max_length=20, choices=[("GEN", "General"), ("OBC", "OBC"), ("SC", "SC"), ("ST", "ST"), ("EWS", "EWS")])
    disability = models.BooleanField(default=False)
    urban_rural = models.CharField(max_length=10, choices=[("URBAN", "Urban"), ("RURAL", "Rural")])

    def __str__(self):
        return f"PII for {self.person.stid} ({self.full_name})"


class ContactPoint(models.Model):
    TYPE_CHOICES = [
        ("MOBILE", "Mobile Phone"),
        ("WHATSAPP", "WhatsApp"),
        ("EMAIL", "Email"),
        ("GUARDIAN_MOBILE", "Guardian Mobile"),
    ]
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="contact_points")
    contact_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value_masked = models.CharField(max_length=50)  # e.g. +91 98****2910
    value_hash = models.CharField(max_length=64, db_index=True)
    is_verified = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=True)
    last_seen_date = models.DateField(auto_now=True)
    churn_count = models.IntegerField(default=0)


class SchemeCrosswalk(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    scheme_trainee_id = models.CharField(max_length=60)  # Scheme specific ID
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="crosswalks")
    enrolled_date = models.DateField()
    certified_date = models.DateField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('scheme', 'scheme_trainee_id')


class ConsentArtefact(models.Model):
    artefact_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="consents")
    notice_version = models.CharField(max_length=20, default="v2.1-DPDP2023")
    language = models.CharField(max_length=10, default="HIN")
    channel = models.CharField(max_length=30, choices=[
        ("MOBILE_OTP", "Mobile OTP"),
        ("E_SIGN", "e-Sign / DigiLocker"),
        ("BIOMETRIC", "Biometric Authentication"),
        ("VOICE_CONSENT", "Voice Assisted Consent"),
    ])
    purpose_flags = models.JSONField(default=dict)
    given_at = models.DateTimeField(auto_now_add=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)
    receipt_hash = models.CharField(max_length=64)
    status = models.CharField(max_length=20, default="ACTIVE")  # ACTIVE, WITHDRAWN, EXPIRED

    def save(self, *args, **kwargs):
        if not self.receipt_hash:
            data_string = f"{self.person_id}:{self.notice_version}:{self.language}:{self.channel}"
            self.receipt_hash = hashlib.sha256(data_string.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)


class Employer(models.Model):
    employer_id = models.CharField(max_length=30, primary_key=True)  # EMP-XX-XXXXX
    legal_name = models.CharField(max_length=255)
    cin_or_gstin = models.CharField(max_length=30)
    udyam_reg = models.CharField(max_length=30, blank=True)
    sector = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    trust_score = models.FloatField(default=0.88)
    is_verified_badge = models.BooleanField(default=True)
    fraud_flag = models.BooleanField(default=False)
    fraud_reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.legal_name} ({self.employer_id})"


class OutcomeEpisode(models.Model):
    KIND_CHOICES = [
        ("WAGE_EMPLOYMENT", "Wage Employment"),
        ("SELF_EMPLOYMENT", "Self Employment"),
        ("APPRENTICESHIP", "Registered Apprenticeship"),
        ("HIGHER_EDUCATION", "Further Education"),
        ("NOT_EMPLOYED", "Not Employed"),
        ("UNKNOWN_UNREACHABLE", "Unknown / Unreachable"),
    ]
    TIER_CHOICES = [
        ("A", "Tier A: Statutory Registry / Verified Document"),
        ("B", "Tier B: Employer Confirmed / Provider Verified"),
        ("C", "Tier C: Corroborated Self-Report"),
        ("D", "Tier D: Unverified Self-Report"),
        ("U", "Tier U: Unknown / Unreachable"),
    ]
    WAGE_BANDS = [
        ("BELOW_MIN_WAGE", "Below Minimum Wage"),
        ("1.0X_TO_1.5X", "1.0x to 1.5x Minimum Wage"),
        ("1.5X_TO_2.0X", "1.5x to 2.0x Minimum Wage"),
        ("ABOVE_2.0X", "Above 2.0x Minimum Wage"),
        ("NOT_APPLICABLE", "Not Applicable"),
    ]

    episode_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="outcome_episodes")
    kind = models.CharField(max_length=30, choices=KIND_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    employer = models.ForeignKey(Employer, null=True, blank=True, on_delete=models.SET_NULL)
    nco_code = models.CharField(max_length=20, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    wage_band = models.CharField(max_length=30, choices=WAGE_BANDS, default="1.0X_TO_1.5X")
    monthly_wage_inr = models.IntegerField(default=0)
    tier = models.CharField(max_length=1, choices=TIER_CHOICES)
    tier_source = models.CharField(max_length=100)  # e.g. EPFO_REGISTRY, EMPLOYER_3TAP, etc.
    rules_version = models.CharField(max_length=20, default="v2.0_NAT")
    non_placement_reason = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.person.stid} - {self.kind} (Tier {self.tier})"


class EvidenceItem(models.Model):
    EVIDENCE_KINDS = [
        ("EPFO_HASH_CONFIRMED", "EPFO UAN / Contribution Hash Match"),
        ("EMPLOYER_3TAP_CONFIRMED", "Direct Employer 3-Tap Web Verification"),
        ("SALARY_SLIP_VERIFIED", "Salary Slip Bank Credit OCR Proof"),
        ("UDYAM_REGISTRATION", "Udyam MSME Registration Certificate"),
        ("BANK_UPI_MERCHANT", "UPI Merchant QR Transaction History"),
        ("APPRENTICE_PORTAL_CONTRACT", "NAPS/NATS Active Apprenticeship Contract"),
        ("SELF_SURVEY_RESPONSE", "Consented Micro-Survey Response"),
    ]
    episode = models.ForeignKey(OutcomeEpisode, on_delete=models.CASCADE, related_name="evidence_items")
    kind = models.CharField(max_length=40, choices=EVIDENCE_KINDS)
    document_ref = models.CharField(max_length=100)  # Token / Hash / Archive Key
    verified_by = models.CharField(max_length=100)
    verified_at = models.DateTimeField(auto_now_add=True)


class VerificationRequest(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="verification_requests")
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    episode = models.ForeignKey(OutcomeEpisode, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default="PENDING")  # PENDING, CONFIRMED, DENIED, EXPIRED
    is_currently_employed = models.BooleanField(null=True, blank=True)
    confirmed_start_date = models.DateField(null=True, blank=True)
    confirmed_wage_band = models.CharField(max_length=30, blank=True)
    skill_rating = models.IntegerField(null=True, blank=True)  # 1 to 5
    response_ip_hash = models.CharField(max_length=64, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)


class FollowUpTask(models.Model):
    WAVE_CHOICES = [
        ("T+30", "T+30 Days Post-Certification"),
        ("T+90", "T+90 Days Post-Certification"),
        ("T+180", "T+180 Days Post-Certification"),
        ("T+365", "T+365 Days Post-Certification"),
        ("T+730", "T+730 Days Post-Certification"),
    ]
    CHANNEL_CHOICES = [
        ("TELEGRAM", "Telegram Automated Bot"),
        ("WHATSAPP", "WhatsApp Cloud API Micro-Survey"),
        ("SMS_LINK", "SMS Short Link Interactive Form"),
        ("IVR_CALL", "Voice IVR / Missed Call System"),
        ("ASSISTED_CALL", "Assisted Call Workbench (Field Agent)"),
        ("FIELD_VISIT", "Physical In-Person Verification"),
    ]
    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("SENT", "Dispatched"),
        ("ANSWERED", "Answered / Completed"),
        ("NO_RESPONSE", "No Response"),
        ("ESCALATED", "Escalated to Next Channel"),
        ("UNREACHABLE", "Marked Unreachable"),
    ]

    task_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="followup_tasks")
    wave = models.CharField(max_length=10, choices=WAVE_CHOICES)
    due_date = models.DateField()
    channel_current = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default="TELEGRAM")
    escalation_step = models.IntegerField(default=1)  # 1 to 6
    attempts_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="SCHEDULED")
    response_propensity_score = models.FloatField(default=0.72)
    intensive_subsample = models.BooleanField(default=False)
    last_attempt_at = models.DateTimeField(null=True, blank=True)


class SurveyResponse(models.Model):
    task = models.ForeignKey(FollowUpTask, on_delete=models.CASCADE, related_name="responses")
    channel = models.CharField(max_length=20)
    employment_status = models.CharField(max_length=50)
    employer_name = models.CharField(max_length=200, blank=True)
    wage_reported = models.IntegerField(default=0)
    non_placement_reason_raw = models.TextField(blank=True)
    reason_nlp_classified = models.CharField(max_length=100, blank=True)
    disposition_code = models.CharField(max_length=30, choices=[
        ("COMPLETE", "Survey Complete"),
        ("CALL_BACK_LATER", "Callback Requested"),
        ("WRONG_NUMBER", "Wrong Number / Changed SIM"),
        ("REFUSED", "Refused Response"),
        ("DECEASED", "Deceased"),
        ("LANGUAGE_BARRIER", "Regional Language Barrier"),
    ], default="COMPLETE")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)


class IdentityMatchQueue(models.Model):
    """
    Human review queue for probabilistic identity scores in the grey band (0.75 to 0.92)
    """
    candidate_a = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="match_candidates_a")
    candidate_b = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="match_candidates_b")
    match_score = models.FloatField()
    match_reasons = models.TextField()
    status = models.CharField(max_length=30, choices=[
        ("PENDING_REVIEW", "Pending Human Review"),
        ("MERGED", "Resolved: Merged as Same Person"),
        ("REJECTED_DISTINCT", "Resolved: Distinct Persons"),
    ], default="PENDING_REVIEW")
    reviewed_by = models.CharField(max_length=100, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)


class ActionCase(models.Model):
    SEVERITY_CHOICES = [
        ("CRITICAL", "Critical Action Required"),
        ("HIGH", "High Priority"),
        ("MEDIUM", "Medium Priority"),
        ("LOW", "Informational Advisory"),
    ]
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "Investigation In Progress"),
        ("REMEDIATED", "Corrective Action Applied"),
        ("CLOSED_WITH_EVIDENCE", "Closed with Audit Evidence"),
    ]

    case_id = models.CharField(max_length=40, primary_key=True)  # CASE-YYYY-XX-NNN
    rule_id = models.CharField(max_length=60)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    assignee = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="OPEN")
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    corrective_action_log = models.TextField(blank=True)


class AuditEvent(models.Model):
    actor = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    target_object = models.CharField(max_length=100)
    purpose = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    prev_hash = models.CharField(max_length=64)
    event_hash = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        if not self.prev_hash:
            last = AuditEvent.objects.order_by('-id').first()
            self.prev_hash = last.event_hash if last else "GENESIS_BLOCK_SKILLTRACE_INDIA_2026"
        data_to_hash = f"{self.prev_hash}:{self.actor}:{self.action}:{self.target_object}:{self.purpose}"
        self.event_hash = hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)
