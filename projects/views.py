from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from skills.models import Skill, UserSkill
from .models import ProjectSubmission

@login_required
def project_list(request):
    submissions = ProjectSubmission.objects.filter(user=request.user)
    skills = Skill.objects.all()
    return render(request, 'projects/project_list.html', {
        'submissions': submissions,
        'skills': skills,
    })


@login_required
def submit_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        skill_id = request.POST.get('skill_id')
        description = request.POST.get('description')
        technologies = request.POST.get('technologies')
        github_url = request.POST.get('github_url')
        live_demo_url = request.POST.get('live_demo_url')
        
        skill = get_object_or_404(Skill, id=skill_id)
        
        ProjectSubmission.objects.create(
            user=request.user,
            skill=skill,
            title=title,
            description=description,
            technologies=technologies,
            github_url=github_url,
            live_demo_url=live_demo_url,
            status='pending'
        )
        messages.success(request, f"Project '{title}' submitted for skill verification! Our assessors will review it.")
        return redirect('project_list')
        
    skills = Skill.objects.all()
    return render(request, 'projects/submit_project.html', {'skills': skills})


@login_required
def review_project(request, project_id):
    if not request.user.is_admin_role:
        messages.error(request, "Access restricted to administrators.")
        return redirect('project_list')
        
    project = get_object_or_404(ProjectSubmission, id=project_id)
    if request.method == 'POST':
        score = float(request.POST.get('score', 0))
        status = request.POST.get('status', 'approved')
        feedback = request.POST.get('admin_feedback', '')
        
        project.score = score
        project.status = status
        project.admin_feedback = feedback
        project.reviewed_by = request.user
        project.reviewed_at = timezone.now()
        project.save()
        
        if status == 'approved':
            user_skill, _ = UserSkill.objects.get_or_create(
                user=project.user,
                skill=project.skill,
                defaults={'claimed_level': 1}
            )
            user_skill.project_score = score
            user_skill.last_assessed_at = timezone.now()
            user_skill.recalculate_score()
            
        messages.success(request, f"Project '{project.title}' reviewed successfully ({status}).")
        return redirect('admin_dashboard')
        
    return render(request, 'projects/review_project.html', {'project': project})
