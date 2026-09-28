from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill, UserSkill, Certificate

@login_required
def skills_dashboard(request):
    user = request.user
    user_skills = UserSkill.objects.filter(user=user).select_related('skill')
    all_skills = Skill.objects.all()
    user_skill_ids = [us.skill_id for us in user_skills]
    available_skills = all_skills.exclude(id__in=user_skill_ids)
    certificates = Certificate.objects.filter(user=user).select_related('skill')

    verified_count = user_skills.filter(is_verified=True).count()
    claimed_only_count = user_skills.filter(is_verified=False).count()
    avg_score = 0
    if verified_count > 0:
        avg_score = round(sum(us.verified_score for us in user_skills.filter(is_verified=True)) / verified_count, 1)

    context = {
        'user_skills': user_skills,
        'available_skills': available_skills,
        'certificates': certificates,
        'verified_count': verified_count,
        'claimed_only_count': claimed_only_count,
        'avg_score': avg_score,
    }
    return render(request, 'skills/skills_list.html', context)


@login_required
def claim_skill(request):
    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        claimed_level = request.POST.get('claimed_level', 1)
        skill = get_object_or_404(Skill, id=skill_id)
        
        user_skill, created = UserSkill.objects.get_or_create(
            user=request.user,
            skill=skill,
            defaults={'claimed_level': int(claimed_level)}
        )
        if not created:
            user_skill.claimed_level = int(claimed_level)
            user_skill.save()
            messages.info(request, f"Updated claimed level for {skill.name} to {user_skill.get_claimed_level_display()}.")
        else:
            messages.success(request, f"Added {skill.name} as a claimed skill ({user_skill.get_claimed_level_display()}). Take an assessment to verify it!")
            
    return redirect('skills_dashboard')
