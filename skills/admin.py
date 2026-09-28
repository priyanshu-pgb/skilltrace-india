from django.contrib import admin
from .models import Skill, UserSkill, Certificate

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon_class', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'claimed_level', 'is_verified', 'verified_score', 'verified_level', 'last_assessed_at')
    list_filter = ('is_verified', 'claimed_level', 'verified_level', 'skill')
    search_fields = ('user__username', 'skill__name')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'skill', 'issuer', 'issue_date', 'is_verified')
    list_filter = ('is_verified', 'skill')
    search_fields = ('name', 'user__username', 'issuer')
