import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.utils import timezone
from accounts.models import User
from skills.models import Skill, UserSkill, Certificate
from assessments.models import AssessmentAttempt, PracticalSubmission
from projects.models import ProjectSubmission
from jobs.models import Job, JobRequirement
from training.models import TrainingCourse, TrainingEnrollment
from employment.models import EmploymentRecord

@login_required
def user_dashboard(request):
    user = request.user
    user_skills = UserSkill.objects.filter(user=user).select_related('skill')
    
    # 1. Summary Cards Data
    verified_skills = user_skills.filter(is_verified=True)
    verified_count = verified_skills.count()
    avg_score = round(verified_skills.aggregate(Avg('verified_score'))['verified_score__avg'] or 0.0, 1)
    
    # 2. Job Matches & Gaps
    jobs = Job.objects.filter(is_active=True).prefetch_related('requirements__skill')
    best_match_job = None
    best_match_percent = 0
    top_gaps = []
    
    for job in jobs:
        analysis = job.calculate_match_for_user(user)
        if analysis['match_percentage'] >= best_match_percent:
            best_match_percent = analysis['match_percentage']
            best_match_job = job
            # Collect gaps
            gaps = [d for d in analysis['details'] if not d['meets']]
            if gaps:
                top_gaps = gaps[:3]
                
    # 3. Training Progress
    enrollments = TrainingEnrollment.objects.filter(user=user).select_related('course', 'course__skill')
    total_enrollments = enrollments.count()
    completed_training = enrollments.filter(status='completed').count()
    in_progress_training = enrollments.filter(status='in_progress').count()
    training_pct = round((completed_training / total_enrollments * 100)) if total_enrollments > 0 else 0
    
    # 4. Employment Status
    emp_record, _ = EmploymentRecord.objects.get_or_create(user=user)
    
    # 5. Career Readiness Score (0-100)
    # Calculated as: (Avg Verified Score * 0.4) + (Best Job Match * 0.3) + (Training factor * 0.15) + (Project Factor * 0.15)
    approved_projects = ProjectSubmission.objects.filter(user=user, status='approved').count()
    project_factor = min(approved_projects * 50, 100)
    readiness_score = round(
        (avg_score * 0.40) +
        (best_match_percent * 0.30) +
        (training_pct * 0.15) +
        (project_factor * 0.15)
    )
    readiness_score = min(max(readiness_score, 5), 100) # baseline min 5 for visual gauge
    
    # 6. Chart Data: Claimed vs Verified Scores
    skill_chart_labels = []
    skill_chart_claimed = []
    skill_chart_verified = []
    
    # Mapping level 1-5 to approx score 20-100 for claimed comparison
    level_to_pct = {1: 30, 2: 50, 3: 70, 4: 85, 5: 100}
    for us in user_skills:
        skill_chart_labels.append(us.skill.name)
        skill_chart_claimed.append(level_to_pct.get(us.claimed_level, 30))
        skill_chart_verified.append(us.verified_score if us.is_verified else 0)
        
    # 7. Recommended Courses
    recommended_courses = TrainingCourse.objects.exclude(
        id__in=enrollments.values_list('course_id', flat=True)
    )[:4]
    
    # 8. Activity Timeline
    activities = []
    for att in AssessmentAttempt.objects.filter(user=user, is_completed=True).order_by('-completed_at')[:4]:
        activities.append({
            'title': f"Completed {att.skill.name} Assessment",
            'desc': f"Scored {att.score_percent}% in {att.get_attempt_type_display()}",
            'date': att.completed_at,
            'icon': 'fa-solid fa-clipboard-check',
            'color': 'primary'
        })
    for proj in ProjectSubmission.objects.filter(user=user).order_by('-submitted_at')[:3]:
        activities.append({
            'title': f"Submitted Project '{proj.title}'",
            'desc': f"Status: {proj.get_status_display()} ({proj.skill.name})",
            'date': proj.submitted_at,
            'icon': 'fa-solid fa-diagram-project',
            'color': 'info'
        })
    for enr in enrollments.order_by('-enrolled_at')[:3]:
        activities.append({
            'title': f"Enrolled in {enr.course.name}",
            'desc': f"Status: {enr.get_status_display()} ({enr.progress_percent}%)",
            'date': enr.enrolled_at,
            'icon': 'fa-solid fa-graduation-cap',
            'color': 'success'
        })
    activities = sorted(activities, key=lambda x: x['date'] if x['date'] else timezone.now(), reverse=True)[:6]

    context = {
        'verified_count': verified_count,
        'avg_score': avg_score,
        'best_match_job': best_match_job,
        'best_match_percent': best_match_percent,
        'top_gaps': top_gaps,
        'gap_count': len(top_gaps),
        'total_enrollments': total_enrollments,
        'completed_training': completed_training,
        'training_pct': training_pct,
        'emp_record': emp_record,
        'readiness_score': readiness_score,
        'recommended_courses': recommended_courses,
        'activities': activities,
        'skill_chart_labels': json.dumps(skill_chart_labels),
        'skill_chart_claimed': json.dumps(skill_chart_claimed),
        'skill_chart_verified': json.dumps(skill_chart_verified),
    }
    return render(request, 'user/dashboard.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role:
        return redirect('user_dashboard')
        
    # Filters
    selected_skill = request.GET.get('skill', '')
    selected_status = request.GET.get('status', '')
    
    # 1. Macro KPIs
    total_users = User.objects.filter(role='user').count()
    total_assessments = AssessmentAttempt.objects.filter(is_completed=True).count()
    total_projects = ProjectSubmission.objects.count()
    pending_projects = ProjectSubmission.objects.filter(status='pending').count()
    
    # Employment Stats
    emp_records = EmploymentRecord.objects.all()
    if selected_status:
        emp_records = emp_records.filter(status=selected_status)
        
    employed_count = emp_records.filter(status__in=['employed', 'internship', 'freelancing', 'self_employed']).count()
    employment_rate = round((employed_count / total_users * 100), 1) if total_users > 0 else 0.0
    
    # Average Skill Score
    avg_score_val = UserSkill.objects.filter(is_verified=True).aggregate(Avg('verified_score'))['verified_score__avg'] or 0.0
    avg_skill_score = round(avg_score_val, 1)
    
    # Training Completion Rate
    total_enr = TrainingEnrollment.objects.count()
    comp_enr = TrainingEnrollment.objects.filter(status='completed').count()
    training_completion_rate = round((comp_enr / total_enr * 100), 1) if total_enr > 0 else 0.0
    
    # 2. Charts Data
    # A. Skill Distribution
    skills_qs = Skill.objects.all()
    skill_names = []
    skill_verified_users = []
    skill_avg_scores = []
    
    for s in skills_qs:
        us_qs = UserSkill.objects.filter(skill=s, is_verified=True)
        skill_names.append(s.name)
        skill_verified_users.append(us_qs.count())
        s_avg = us_qs.aggregate(Avg('verified_score'))['verified_score__avg'] or 0.0
        skill_avg_scores.append(round(s_avg, 1))
        
    # B. Employment Status Distribution
    emp_statuses = ['employed', 'internship', 'freelancing', 'self_employed', 'higher_studies', 'unemployed']
    status_labels = ['Employed', 'Internship', 'Freelancing', 'Self-Employed', 'Higher Studies', 'Unemployed']
    status_counts = []
    for st in emp_statuses:
        status_counts.append(EmploymentRecord.objects.filter(status=st).count())
        
    # C. Impact: Before vs After Training Score Improvement
    reassessment_data = TrainingEnrollment.objects.filter(
        status='completed',
        score_before__isnull=False,
        score_after__isnull=False
    ).select_related('course', 'course__skill')[:8]
    
    impact_labels = []
    impact_before = []
    impact_after = []
    total_delta = 0
    delta_count = 0
    
    for r in reassessment_data:
        impact_labels.append(f"{r.course.skill.name} ({r.user.username})")
        impact_before.append(r.score_before)
        impact_after.append(r.score_after)
        total_delta += (r.score_after - r.score_before)
        delta_count += 1
        
    avg_observed_delta = round(total_delta / delta_count, 1) if delta_count > 0 else 0.0

    # D. Common Skill Gaps Analysis
    common_gaps = []
    for s in skills_qs:
        # Check requirement count across jobs vs verified users with that level
        reqs = JobRequirement.objects.filter(skill=s)
        if reqs.exists():
            avg_req_level = reqs.aggregate(Avg('required_level'))['required_level__avg'] or 3.0
            us_s = UserSkill.objects.filter(skill=s, is_verified=True)
            user_avg_lvl = us_s.aggregate(Avg('verified_level'))['verified_level__avg'] or 0.0
            gap_magnitude = round(max(0, avg_req_level - user_avg_lvl), 1)
            common_gaps.append({
                'skill_name': s.name,
                'avg_required_level': round(avg_req_level, 1),
                'user_avg_level': round(user_avg_lvl, 1),
                'gap_magnitude': gap_magnitude,
                'job_count': reqs.count(),
            })
    common_gaps = sorted(common_gaps, key=lambda x: x['gap_magnitude'], reverse=True)

    # Pending project reviews
    pending_submissions = ProjectSubmission.objects.filter(status='pending').select_related('user', 'skill')[:6]

    context = {
        'total_users': total_users,
        'total_assessments': total_assessments,
        'total_projects': total_projects,
        'pending_projects': pending_projects,
        'employed_count': employed_count,
        'employment_rate': employment_rate,
        'avg_skill_score': avg_skill_score,
        'training_completion_rate': training_completion_rate,
        'avg_observed_delta': avg_observed_delta,
        'common_gaps': common_gaps,
        'pending_submissions': pending_submissions,
        'skills_list': skills_qs,
        'selected_skill': selected_skill,
        'selected_status': selected_status,
        
        # Chart JSON
        'skill_names_json': json.dumps(skill_names),
        'skill_verified_users_json': json.dumps(skill_verified_users),
        'skill_avg_scores_json': json.dumps(skill_avg_scores),
        'status_labels_json': json.dumps(status_labels),
        'status_counts_json': json.dumps(status_counts),
        'impact_labels_json': json.dumps(impact_labels),
        'impact_before_json': json.dumps(impact_before),
        'impact_after_json': json.dumps(impact_after),
    }
    return render(request, 'admin_dashboard/dashboard.html', context)
