from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job
from training.models import TrainingCourse

@login_required
def jobs_list(request):
    jobs = Job.objects.filter(is_active=True).prefetch_related('requirements__skill')
    job_cards = []
    
    for job in jobs:
        analysis = job.calculate_match_for_user(request.user)
        job_cards.append({
            'job': job,
            'match_percentage': analysis['match_percentage'],
            'matched_count': analysis['matched_count'],
            'total_count': analysis['total_count'],
            'gap_count': analysis['gap_count'],
        })
        
    return render(request, 'jobs/jobs_list.html', {'job_cards': job_cards})


@login_required
def job_skill_gap_report(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    analysis = job.calculate_match_for_user(request.user)
    
    # Identify skills with gaps to recommend targeted courses
    gap_skills = [item['skill'] for item in analysis['details'] if not item['meets']]
    recommended_courses = TrainingCourse.objects.filter(skill__in=gap_skills)
    
    return render(request, 'jobs/skill_gap_report.html', {
        'job': job,
        'analysis': analysis,
        'recommended_courses': recommended_courses,
    })
