import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from .models import (
    EmploymentRecord,
    LongitudinalMilestone,
    NonPlacementReason,
    FollowUpLog,
    EmployerVerificationRequest,
)

@login_required
def employment_tracker(request):
    user = request.user
    record, _ = EmploymentRecord.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        action = request.POST.get('action', 'update_status')
        
        if action == 'update_status':
            status = request.POST.get('status')
            record.status = status
            
            if status in ['employed', 'internship', 'freelancing', 'self_employed']:
                record.company_name = request.POST.get('company_name', '').strip()
                record.job_role = request.POST.get('job_role', '').strip()
                record.salary_range = request.POST.get('salary_range', '').strip()
                
                # Monthly take-home wage
                wage_val = request.POST.get('current_monthly_wage', '').strip()
                if wage_val and wage_val.isdigit():
                    record.current_monthly_wage = int(wage_val)
                elif wage_val == '':
                    record.current_monthly_wage = None
                    
                record.location = request.POST.get('location', '').strip()
                record.employment_type = request.POST.get('employment_type', 'full_time')
                record.skills_used = request.POST.get('skills_used', '').strip()
                record.training_relevance = request.POST.get('training_relevance', 'high')
                record.epfo_uan = request.POST.get('epfo_uan', '').strip()
                record.employer_gstin = request.POST.get('employer_gstin', '').strip()
                
                joining_date = request.POST.get('joining_date')
                if joining_date:
                    record.joining_date = joining_date
                    
                # Update / sync initial Milestone 0
                wage = record.current_monthly_wage or 15000
                m0, created = LongitudinalMilestone.objects.get_or_create(
                    user=user,
                    milestone_month=0,
                    defaults={
                        'status': status,
                        'company_name': record.company_name,
                        'job_role': record.job_role,
                        'monthly_wage': wage,
                        'is_retained': True,
                        'training_relevance': record.training_relevance,
                        'verification_source': 'employer_confirmed' if record.is_verified_by_admin else 'self_reported',
                        'check_in_date': record.joining_date or timezone.now().date(),
                    }
                )
                if not created:
                    m0.status = status
                    m0.company_name = record.company_name
                    m0.job_role = record.job_role
                    m0.monthly_wage = wage
                    m0.training_relevance = record.training_relevance
                    m0.save()
            else:
                # Candidate is unemployed / seeking / dropped out
                record.company_name = ''
                record.job_role = ''
                record.salary_range = ''
                record.current_monthly_wage = None
                record.location = ''
                record.joining_date = None
                
            record.save()
            messages.success(request, "Career and employment status updated successfully!")
            return redirect('employment_tracker')

    # Fetch longitudinal milestones
    milestones = LongitudinalMilestone.objects.filter(user=user).order_by('milestone_month')
    
    # Calculate wage progression delta if multiple milestones exist
    milestone_list = list(milestones)
    wage_progression = []
    if len(milestone_list) > 1:
        for i in range(len(milestone_list)):
            m = milestone_list[i]
            prev_wage = milestone_list[i-1].monthly_wage if i > 0 else m.monthly_wage
            delta = m.monthly_wage - prev_wage if i > 0 else 0
            wage_progression.append({
                'month': m.milestone_month,
                'wage': m.monthly_wage,
                'delta': delta,
                'status': m.get_status_display(),
                'source': m.get_verification_source_display()
            })

    # Employer verification requests
    verifications = EmployerVerificationRequest.objects.filter(user=user).order_by('-created_at')
    
    # Attrition / Non-placement records
    non_placement_reasons = NonPlacementReason.objects.filter(user=user).order_by('-recorded_at')
    
    # Follow-up logs for trainee
    followup_logs = FollowUpLog.objects.filter(user=user).order_by('-logged_at')[:5]

    context = {
        'record': record,
        'milestones': milestones,
        'wage_progression': wage_progression,
        'verifications': verifications,
        'non_placement_reasons': non_placement_reasons,
        'followup_logs': followup_logs,
    }
    return render(request, 'employment/tracker.html', context)


@login_required
def record_milestone(request):
    """Adds a longitudinal retention milestone (Month 3, 6, 12, 24)."""
    if request.method == 'POST':
        user = request.user
        try:
            month = int(request.POST.get('milestone_month', 3))
            wage = int(request.POST.get('monthly_wage', 15000))
        except (ValueError, TypeError):
            month = 3
            wage = 15000
            
        status = request.POST.get('status', 'employed')
        company = request.POST.get('company_name', '').strip()
        role = request.POST.get('job_role', '').strip()
        relevance = request.POST.get('training_relevance', 'high')
        source = request.POST.get('verification_source', 'self_reported')
        notes = request.POST.get('notes', '').strip()
        
        # Check previous milestone to determine if wage increased
        prev_milestones = LongitudinalMilestone.objects.filter(user=user, milestone_month__lt=month).order_by('-milestone_month')
        is_increased = False
        if prev_milestones.exists():
            prev = prev_milestones.first()
            is_increased = (wage > prev.monthly_wage)
            
        milestone, created = LongitudinalMilestone.objects.update_or_create(
            user=user,
            milestone_month=month,
            defaults={
                'status': status,
                'company_name': company,
                'job_role': role,
                'monthly_wage': wage,
                'is_retained': (status in ['employed', 'internship', 'freelancing', 'self_employed']),
                'is_wage_increased': is_increased,
                'training_relevance': relevance,
                'verification_source': source,
                'check_in_date': timezone.now().date(),
                'notes': notes,
            }
        )
        
        # Update main record
        record, _ = EmploymentRecord.objects.get_or_create(user=user)
        record.status = status
        record.company_name = company
        record.job_role = role
        record.current_monthly_wage = wage
        record.last_milestone_month = max(record.last_milestone_month, month)
        record.training_relevance = relevance
        record.save()
        
        messages.success(request, f"Month {month} Longitudinal Milestone recorded with monthly wage ₹{wage:,}!")
    return redirect('employment_tracker')


@login_required
def record_non_placement(request):
    """Records systemic reasons for non-placement or attrition with remediation suggestion."""
    if request.method == 'POST':
        user = request.user
        category = request.POST.get('category', 'other')
        details = request.POST.get('details', '').strip()
        
        # Policy & counseling recommendations based on Indian vocational context
        recommendation_map = {
            'relocation_refusal': 'Recommend local MSME cluster apprenticeship or remote tele-work opportunities within home district.',
            'wage_dissatisfaction': 'Evaluate eligibility for post-placement migration support stipend (under PMKVY/DDU-GKY) and negotiate entry level incentives.',
            'family_marriage': 'Offer flexible home-based or hybrid livelihood skilling (e.g. self-employment/SHG linkage under NRLM).',
            'skill_mismatch': 'Schedule 40-hour targeted practical remedial module and mock interviews with industry assessor.',
            'local_opportunity_lack': 'Liaise with District Skill Committee (DSC) to bridge local industrial vacancies with candidate profile.',
            'health_personal': 'Put candidate on temporary health sabbatical with scheduled re-engagement in 60 days.',
            'joined_informal': 'Counsel candidate on formal sector benefits (EPFO, ESIC, career progression) vs immediate cash daily wage.',
            'higher_education': 'Register on Alumni & Continuing Education register for weekend advanced modules.',
        }
        action = recommendation_map.get(category, 'Schedule counseling session with Rozgar Sahayak.')
        
        NonPlacementReason.objects.create(
            user=user,
            category=category,
            details=details,
            recommended_action=action,
        )
        
        # Update employment record status if not already set
        record, _ = EmploymentRecord.objects.get_or_create(user=user)
        if record.status in ['employed', 'internship', 'freelancing', 'self_employed']:
            record.status = 'dropped_out'
            record.save()
            
        messages.info(request, f"Outcome recorded. System recommendation: {action}")
    return redirect('employment_tracker')


@login_required
def request_employer_verification(request):
    """Generates a low-burden 1-click tokenized verification link for the employer."""
    if request.method == 'POST':
        user = request.user
        company = request.POST.get('company_name', '').strip()
        contact_name = request.POST.get('employer_contact_name', '').strip()
        email = request.POST.get('employer_email', '').strip()
        phone = request.POST.get('employer_phone', '').strip()
        
        verif_req = EmployerVerificationRequest.objects.create(
            user=user,
            company_name=company,
            employer_contact_name=contact_name,
            employer_email=email,
            employer_phone=phone,
            status='pending',
        )
        
        verify_url = request.build_absolute_uri(reverse('public_employer_verify', kwargs={'token': verif_req.token}))
        messages.success(request, f"1-Click Employer Verification Link generated! Share with your HR/Manager: {verify_url}")
    return redirect('employment_tracker')


def public_employer_verify(request, token):
    """
    Public 1-click employer outcome validation page (No login required).
    Allows HR/Employer to verify employment in 30 seconds.
    """
    verif_req = get_object_or_404(EmployerVerificationRequest, token=token)
    candidate = verif_req.user
    
    if request.method == 'POST':
        role = request.POST.get('confirmed_role', '').strip()
        wage_str = request.POST.get('confirmed_monthly_wage', '').strip()
        joining_date = request.POST.get('confirmed_joining_date')
        gstin = request.POST.get('gstin', '').strip()
        has_epfo = request.POST.get('has_epfo_coverage') == 'on'
        feedback = request.POST.get('feedback_on_trainee', '').strip()
        
        wage = int(wage_str) if wage_str and wage_str.isdigit() else 18000
        
        verif_req.status = 'confirmed'
        verif_req.confirmed_role = role
        verif_req.confirmed_monthly_wage = wage
        if joining_date:
            verif_req.confirmed_joining_date = joining_date
        verif_req.gstin = gstin
        verif_req.has_epfo_coverage = has_epfo
        verif_req.feedback_on_trainee = feedback
        verif_req.responded_at = timezone.now()
        verif_req.save()
        
        # Automatically update candidate's EmploymentRecord
        record, _ = EmploymentRecord.objects.get_or_create(user=candidate)
        record.status = 'employed'
        record.company_name = verif_req.company_name
        record.job_role = role
        record.current_monthly_wage = wage
        if joining_date:
            record.joining_date = joining_date
        record.is_verified_by_admin = True
        record.employer_gstin = gstin
        if has_epfo:
            record.epfo_uan = 'EPFO-VERIFIED-SIGNAL'
        record.save()
        
        # Also create or update verified milestone
        LongitudinalMilestone.objects.update_or_create(
            user=candidate,
            milestone_month=0,
            defaults={
                'status': 'employed',
                'company_name': verif_req.company_name,
                'job_role': role,
                'monthly_wage': wage,
                'is_retained': True,
                'training_relevance': 'high',
                'verification_source': 'employer_confirmed',
                'check_in_date': timezone.now().date(),
                'notes': f"Direct Employer 1-Click Verification via {verif_req.employer_contact_name or 'HR'}. GSTIN: {gstin}. EPFO: {has_epfo}",
            }
        )
        
        return render(request, 'employment/verify_success.html', {
            'verif_req': verif_req,
            'candidate': candidate,
        })
        
    return render(request, 'employment/verify_employer.html', {
        'verif_req': verif_req,
        'candidate': candidate,
    })


@login_required
def quick_checkin_simulate(request):
    """
    Simulates automated WhatsApp / SMS conversational check-in.
    Provides low-burden 30-second response logging.
    """
    user = request.user
    if request.method == 'POST':
        status = request.POST.get('status', 'employed')
        wage_str = request.POST.get('monthly_wage', '16000')
        wage = int(wage_str) if wage_str.isdigit() else 16000
        relevance = request.POST.get('training_relevance', 'high')
        channel = request.POST.get('channel', 'whatsapp_bot')
        phone = request.POST.get('contact_phone', user.phone or '9876543210')
        alt_phone = request.POST.get('alt_phone', user.alt_phone or '')
        
        # Update user's alternative phone if provided
        if alt_phone:
            user.alt_phone = alt_phone
            user.save()
            
        # Log the follow-up interaction
        FollowUpLog.objects.create(
            user=user,
            channel=channel,
            contact_number_used=phone,
            contact_type='primary',
            status='responded',
            response_text=f"Auto-parsed: Status={status}, Wage=₹{wage}, Relevance={relevance}",
        )
        
        # Calculate milestone month based on current status
        record, _ = EmploymentRecord.objects.get_or_create(user=user)
        next_month = 6 if record.last_milestone_month < 6 else 12
        if record.last_milestone_month >= 12:
            next_month = 24
            
        LongitudinalMilestone.objects.update_or_create(
            user=user,
            milestone_month=next_month,
            defaults={
                'status': status,
                'company_name': record.company_name or 'Livelihood Engagement',
                'job_role': record.job_role or 'Skilled Technician',
                'monthly_wage': wage,
                'is_retained': (status in ['employed', 'internship', 'freelancing', 'self_employed']),
                'training_relevance': relevance,
                'verification_source': 'self_reported',
                'check_in_date': timezone.now().date(),
                'notes': f"Recorded via {channel} low-burden check-in.",
            }
        )
        record.current_monthly_wage = wage
        record.last_milestone_month = next_month
        record.training_relevance = relevance
        record.save()
        
        messages.success(request, f"WhatsApp Check-in recorded! Month {next_month} milestone updated with ₹{wage:,}/month.")
        return redirect('employment_tracker')
        
    return render(request, 'employment/whatsapp_checkin.html', {'user': user})


@login_required
def admin_outreach_console(request):
    """
    Administrative console for tracking multi-channel follow-ups,
    trainee contact drift, and employer confirmation health.
    """
    if not request.user.is_admin_role:
        return redirect('user_dashboard')
        
    followups = FollowUpLog.objects.select_related('user').all()[:50]
    employer_verifs = EmployerVerificationRequest.objects.select_related('user').all()[:50]
    unreachable_count = FollowUpLog.objects.filter(status__in=['unreachable', 'wrong_number']).count()
    responded_count = FollowUpLog.objects.filter(status='responded').count()
    confirmed_employer_count = EmployerVerificationRequest.objects.filter(status='confirmed').count()
    total_verif_requests = EmployerVerificationRequest.objects.count()
    
    employer_confirmation_rate = round((confirmed_employer_count / total_verif_requests * 100), 1) if total_verif_requests > 0 else 0.0

    context = {
        'followups': followups,
        'employer_verifs': employer_verifs,
        'unreachable_count': unreachable_count,
        'responded_count': responded_count,
        'confirmed_employer_count': confirmed_employer_count,
        'total_verif_requests': total_verif_requests,
        'employer_confirmation_rate': employer_confirmation_rate,
    }
    return render(request, 'employment/admin_outreach.html', context)
