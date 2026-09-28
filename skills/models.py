from django.db import models
from django.conf import settings

def score_to_level(score):
    """Converts a numeric score (0-100) to level integer (1-5) and string label."""
    if score >= 90:
        return 5, 'Expert'
    elif score >= 75:
        return 4, 'Advanced'
    elif score >= 60:
        return 3, 'Intermediate'
    elif score >= 40:
        return 2, 'Basic'
    else:
        return 1, 'Beginner'

def level_num_to_name(level_num):
    mapping = {
        1: 'Beginner',
        2: 'Basic',
        3: 'Intermediate',
        4: 'Advanced',
        5: 'Expert',
    }
    return mapping.get(level_num, 'Unassessed')


class Skill(models.Model):
    CATEGORY_CHOICES = (
        ('tech', 'Technical / Programming'),
        ('data', 'Data & Analytics'),
        ('design', 'UI/UX & Design'),
        ('soft', 'Soft Skills & Leadership'),
        ('tools', 'Tools & Platforms'),
    )
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='tech')
    description = models.TextField(blank=True, default='')
    icon_class = models.CharField(max_length=50, default='fa-solid fa-code', help_text='Font Awesome icon class')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    LEVEL_CHOICES = (
        (1, 'Beginner'),
        (2, 'Basic'),
        (3, 'Intermediate'),
        (4, 'Advanced'),
        (5, 'Expert'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills')
    
    # Claimed vs Verified distinction
    claimed_level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=1)
    is_verified = models.BooleanField(default=False)
    
    # Verification details
    verified_score = models.FloatField(default=0.0, help_text="Aggregated verified score 0-100")
    verified_level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=1)
    
    # Component breakdown scores
    mcq_score = models.FloatField(default=0.0)
    practical_score = models.FloatField(default=0.0)
    project_score = models.FloatField(default=0.0)
    viva_score = models.FloatField(default=0.0)

    # History & Timestamping
    verified_at = models.DateTimeField(null=True, blank=True)
    last_assessed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'skill')
        ordering = ['-is_verified', '-verified_score', 'skill__name']

    def __str__(self):
        status = f"Verified ({self.verified_score}%)" if self.is_verified else f"Claimed ({self.get_claimed_level_display()})"
        return f"{self.user.username} - {self.skill.name}: {status}"

    @property
    def claimed_level_name(self):
        return level_num_to_name(self.claimed_level)

    @property
    def verified_level_name(self):
        if not self.is_verified:
            return "Unverified"
        return level_num_to_name(self.verified_level)

    def recalculate_score(self, mcq_weight=0.20, practical_weight=0.50, project_weight=0.30, viva_weight=0.0):
        """Calculates normalized score server-side per Section 33."""
        final_score = (
            (self.mcq_score * mcq_weight) +
            (self.practical_score * practical_weight) +
            (self.project_score * project_weight) +
            (self.viva_score * viva_weight)
        )
        self.verified_score = round(min(max(final_score, 0.0), 100.0), 1)
        self.verified_level, _ = score_to_level(self.verified_score)
        self.is_verified = (self.mcq_score > 0 or self.practical_score > 0 or self.project_score > 0)
        self.save()
        return self.verified_score


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_date = models.DateField()
    certificate_url = models.URLField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
