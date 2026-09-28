from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmploymentRecord

@login_required
def employment_tracker(request):
    record, _ = EmploymentRecord.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        record.status = status
        
        if status in ['employed', 'internship', 'freelancing', 'self_employed']:
            record.company_name = request.POST.get('company_name', '').strip()
            record.job_role = request.POST.get('job_role', '').strip()
            record.salary_range = request.POST.get('salary_range', '').strip()
            record.location = request.POST.get('location', '').strip()
            record.employment_type = request.POST.get('employment_type', 'full_time')
            record.skills_used = request.POST.get('skills_used', '').strip()
            joining_date = request.POST.get('joining_date')
            if joining_date:
                record.joining_date = joining_date
        else:
            # Clear employment details if unemployed / higher studies
            record.company_name = ''
            record.job_role = ''
            record.salary_range = ''
            record.location = ''
            record.joining_date = None
            
        record.save()
        messages.success(request, "Employment status updated successfully!")
        return redirect('employment_tracker')
        
    return render(request, 'employment/tracker.html', {'record': record})
