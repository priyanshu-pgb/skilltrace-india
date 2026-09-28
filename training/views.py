from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from skills.models import Skill, UserSkill
from .models import TrainingCourse, TrainingEnrollment

@login_required
def training_catalog(request):
    courses = TrainingCourse.objects.all().select_related('skill')
    user_enrolled_ids = TrainingEnrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    
    # Recommend courses based on user's unverified or lower-level skills
    user_skills = UserSkill.objects.filter(user=request.user)
    low_skill_ids = [us.skill_id for us in user_skills if (not us.is_verified) or (us.verified_level < 4)]
    recommended = courses.filter(skill_id__in=low_skill_ids)
    
    return render(request, 'training/catalog.html', {
        'courses': courses,
        'user_enrolled_ids': list(user_enrolled_ids),
        'recommended': recommended,
    })


@login_required
def my_training(request):
    enrollments = TrainingEnrollment.objects.filter(user=request.user).select_related('course', 'course__skill')
    return render(request, 'training/my_training.html', {'enrollments': enrollments})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(TrainingCourse, id=course_id)
    
    # Capture current baseline score for the skill
    current_skill = UserSkill.objects.filter(user=request.user, skill=course.skill).first()
    baseline_score = current_skill.verified_score if current_skill else 0.0
    
    enrollment, created = TrainingEnrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={
            'status': 'in_progress',
            'progress_percent': 10,
            'score_before': baseline_score,
        }
    )
    if created:
        messages.success(request, f"Enrolled in '{course.name}'! Baseline score recorded: {baseline_score}%.")
    else:
        messages.info(request, f"You are already enrolled in '{course.name}'.")
        
    return redirect('my_training')


@login_required
def update_progress(request, enrollment_id):
    enrollment = get_object_or_404(TrainingEnrollment, id=enrollment_id, user=request.user)
    if request.method == 'POST':
        new_progress = int(request.POST.get('progress_percent', 0))
        new_progress = min(max(new_progress, 0), 100)
        enrollment.progress_percent = new_progress
        
        if new_progress == 100 and enrollment.status != 'completed':
            enrollment.status = 'completed'
            enrollment.completed_at = timezone.now()
            messages.success(request, f"Congratulations! You completed '{enrollment.course.name}'! You are now eligible for Re-Assessment.")
        elif new_progress > 0:
            enrollment.status = 'in_progress'
            messages.info(request, f"Training progress updated to {new_progress}%.")
            
        enrollment.save()
        
    return redirect('my_training')


@login_required
def reassessment_overview(request):
    """Shows all courses completed and before/after score delta per Prompt Section 42."""
    enrollments = TrainingEnrollment.objects.filter(user=request.user).select_related('course', 'course__skill')
    
    # Sync latest verified score to score_after if user re-assessed
    comparison_data = []
    for enr in enrollments:
        curr_us = UserSkill.objects.filter(user=request.user, skill=enr.course.skill).first()
        if curr_us and enr.status == 'completed':
            if enr.score_after is None or enr.score_after != curr_us.verified_score:
                enr.score_after = curr_us.verified_score
                enr.save()
        
        comparison_data.append({
            'enrollment': enr,
            'before': enr.score_before or 0.0,
            'after': enr.score_after if enr.score_after is not None else curr_us.verified_score if curr_us else 0.0,
            'delta': round((enr.score_after or (curr_us.verified_score if curr_us else 0.0)) - (enr.score_before or 0.0), 1),
            'skill': enr.course.skill,
        })
        
    return render(request, 'training/reassessment.html', {'comparison_data': comparison_data})
