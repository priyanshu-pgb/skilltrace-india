from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('SkillBridge Attributes', {'fields': ('role', 'phone', 'location')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('SkillBridge Attributes', {'fields': ('role', 'phone', 'location')}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'institution', 'graduation_year', 'target_role', 'updated_at')
    search_fields = ('user__username', 'user__email', 'degree', 'institution', 'target_role')
