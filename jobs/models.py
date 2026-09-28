from django.db import models
from skills.models import Skill, level_num_to_name

class Job(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    department = models.CharField(max_length=100, default='Technology')
    description = models.TextField()
    experience_level = models.CharField(max_length=50, default='Entry / Associate')
    salary_range = models.CharField(max_length=100, default='₹6,00,000 - ₹10,00,000 PA')
    location = models.CharField(max_length=100, default='Hybrid / Remote')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def calculate_match_for_user(self, user):
        """Calculates exact skill gap analysis for a specific user."""
        requirements = self.requirements.select_related('skill').all()
        if not requirements:
            return {'match_percentage': 0, 'details': [], 'matched_count': 0, 'total_count': 0, 'gap_count': 0}

        user_skills_map = {
            us.skill_id: (us.verified_level if us.is_verified else 0)
            for us in user.user_skills.all()
        }

        matched_count = 0
        total_count = requirements.count()
        details = []

        for req in requirements:
            user_level = user_skills_map.get(req.skill_id, 0)
            gap = req.required_level - user_level
            meets = (gap <= 0)
            if meets:
                matched_count += 1

            details.append({
                'skill': req.skill,
                'required_level_num': req.required_level,
                'required_level_name': level_num_to_name(req.required_level),
                'user_level_num': user_level,
                'user_level_name': level_num_to_name(user_level) if user_level > 0 else 'Not Verified',
                'gap': max(0, gap),
                'meets': meets,
            })

        match_percentage = round((matched_count / total_count) * 100.0) if total_count > 0 else 0
        gap_count = total_count - matched_count

        return {
            'match_percentage': match_percentage,
            'details': details,
            'matched_count': matched_count,
            'total_count': total_count,
            'gap_count': gap_count,
        }


class JobRequirement(models.Model):
    LEVEL_CHOICES = (
        (1, 'Beginner'),
        (2, 'Basic'),
        (3, 'Intermediate'),
        (4, 'Advanced'),
        (5, 'Expert'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='requirements')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='job_requirements')
    required_level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=3)
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        unique_together = ('job', 'skill')

    def __str__(self):
        return f"{self.job.title} requires {self.skill.name} ({self.get_required_level_display()})"
