import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def landing(request):
    """Modern interactive landing page for SOPAN."""
    return render(request, 'landing.html', {'is_public_page': True})

def health_check(request):
    """Health check endpoint for deployment and validation."""
    return JsonResponse({'status': 'healthy', 'service': 'SOPAN', 'version': '2.0.0'})

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def custom_403(request, exception=None):
    return render(request, '403.html', status=403)

def custom_500(request):
    return render(request, '500.html', status=500)

def privacy_policy(request):
    """India DPDP Act 2023 & IT Act 2000 compliant Privacy Policy page."""
    return render(request, 'legal/privacy_policy.html', {'is_public_page': True})

def terms_conditions(request):
    """Official Terms and Conditions with Non-Employment Guarantee disclaimer."""
    return render(request, 'legal/terms_conditions.html', {'is_public_page': True})

def cookie_policy(request):
    """Detailed Cookie & Local Storage transparency policy."""
    return render(request, 'legal/cookie_policy.html', {'is_public_page': True})

def refund_policy(request):
    """Transparent Refund & Cancellation terms (100% free candidate guarantee)."""
    return render(request, 'legal/refund_policy.html', {'is_public_page': True})

def grievance_redressal(request):
    """Statutory Grievance Redressal and Data Protection Officer page."""
    return render(request, 'legal/grievance_redressal.html', {'is_public_page': True})


@csrf_exempt
def chat_assistant_api(request):
    """
    Intelligent Conversational AI Assistant API for SOPAN.
    Answers candidate & administrator queries, provides recommendations, and directs action.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            msg = data.get('message', '').strip().lower()
        except Exception:
            msg = request.POST.get('message', '').strip().lower()
            
        user = request.user if request.user.is_authenticated else None
        user_name = user.first_name or user.username if user else "Candidate"
        is_admin = getattr(user, 'is_admin_role', False) if user else False
        
        reply = ""
        action_link = None
        action_text = None
        
        # 1. Greetings & Identity
        if any(w in msg for w in ['hello', 'hi', 'hey', 'namaste', 'start', 'who are you']):
            if is_admin:
                reply = f"Namaste Administrator! I'm Trainer Vikram. I monitor nationwide skilling cohorts, provider accountability rankings, and 6-month retention curves. How can I assist your command center today?"
                action_link = "/admin-dashboard/"
                action_text = "Open National Command Center"
            else:
                reply = f"Namaste {user_name}! I'm Mentor Maya, your SOPAN career ladder guide. Ask me anything about testing your skills, finding high-paying job matches, 1-click employer audits, or logging your 3-month wage hikes!"
                action_link = "/user-dashboard/"
                action_text = "Explore My Dashboard"
                
        # 2. Testing & Skill Verification
        elif any(w in msg for w in ['test', 'assess', 'quiz', 'score', 'mcq', 'practical', 'code', 'verify']):
            reply = "In SOPAN, skills are verified through 3 balanced weights: Practical Coding (50%), MCQs (20%), and Projects (30%). A verified badge boosts your target job match by up to +40 points!"
            action_link = "/assessments/"
            action_text = "Take 5-Min Skill Test"
            
        # 3. Wage Progression & Longitudinal Milestones
        elif any(w in msg for w in ['wage', 'salary', 'money', 'hike', 'milestone', 'progression', 'month', 'livelihood']):
            reply = "SOPAN tracks your upward mobility at Month 0, 3, 6, 12, and 24! For example, candidate Priya Nair logged her journey from ₹18,000 to ₹28,000/month. Ready to log your current milestone?"
            action_link = "/employment/"
            action_text = "Log Retention Milestone"
            
        # 4. 1-Click Employer Verification
        elif any(w in msg for w in ['employer', 'hr', 'audit', 'token', 'epfo', 'gstin']):
            reply = "Our 1-Click Employer Verification lets you generate a tokenized link for your HR or Manager. They can verify your designation, monthly wage, and EPFO status in 30 seconds with no password needed!"
            action_link = "/employment/"
            action_text = "Generate Employer Link"
            
        # 5. Job Matching & Skill Gaps
        elif any(w in msg for w in ['job', 'gap', 'vacanc', 'opening', 'match', 'career', 'role']):
            reply = "Our Mathematical Gap Engine compares your verified levels with real industry requirements. It highlights your friction gaps and immediately maps you to the right skilling module."
            action_link = "/jobs/"
            action_text = "View Active Job Gaps"
            
        # 6. Training & Schemes
        elif any(w in msg for w in ['train', 'course', 'pmkvy', 'naps', 'ddu', 'learn', 'vishwakarma']):
            reply = "We offer curriculum tracks linked to PMKVY 4.0, NAPS Apprenticeships, and PM-Vishwakarma. All courses feature pre-training baselines and post-training re-assessments to measure your exact improvement delta!"
            action_link = "/training/"
            action_text = "Browse Training Courses"
            
        # 7. WhatsApp Bot & Contact Drift
        elif any(w in msg for w in ['whatsapp', 'bot', 'quick', 'phone', 'sim', 'contact', 'disconnect']):
            reply = "You can update your career progress in 30 seconds via our conversational WhatsApp bot! It also secures an alternate village/guardian contact so you never lose connection."
            action_link = "/employment/quick-checkin/"
            action_text = "Open 30s WhatsApp Bot"
            
        # 8. District & Aspirational Districts
        elif any(w in msg for w in ['district', 'aspirational', 'provider', 'ranchi', 'nuh', 'khurda', 'state']):
            reply = "SOPAN benchmarks outcomes across NITI Aayog Aspirational Districts (like Ranchi, Nuh, and Khurda) to ensure skilling funds reach underserved rural and tribal youth."
            action_link = "/admin-dashboard/"
            action_text = "Inspect District Analytics"
            
        # 9. Problems, Relocation & Counseling
        elif any(w in msg for w in ['problem', 'stuck', 'relocat', 'unemployed', 'help', 'drop', 'marriage', 'family']):
            reply = "Facing challenges with migration, low salary, or family constraints? Report it in the Placement Support module. SOPAN automatically triggers local district apprenticeship linkages and counseling!"
            action_link = "/employment/"
            action_text = "Submit for District Support"
            
        # 10. Default / Fallback
        else:
            if is_admin:
                reply = "I'm Trainer Vikram. You can ask me about training partner rankings, longitudinal retention curves, 1-click employer audit rates, or SIM churn mitigation logs."
                action_link = "/admin-dashboard/"
                action_text = "National Command Center"
            else:
                reply = f"Great question! SOPAN (सोपान) is your ladder to verified skills and higher wages. Would you like to verify a skill, check your job gaps, or log your latest wage milestone?"
                action_link = "/user-dashboard/"
                action_text = "Go to Candidate Hub"
                
        return JsonResponse({
            'status': 'ok',
            'reply': reply,
            'action_link': action_link,
            'action_text': action_text,
            'sender': 'Trainer Vikram' if is_admin else 'Mentor Maya',
            'avatar': '/static/images/trainer_admin.svg' if is_admin else '/static/images/mentor_student.svg',
        })
        
    return JsonResponse({'error': 'POST required'}, status=405)
