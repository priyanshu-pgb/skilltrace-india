from django.shortcuts import render
from django.http import JsonResponse

def landing(request):
    """Modern interactive landing page for SkillBridge."""
    return render(request, 'landing.html')

def health_check(request):
    """Health check endpoint for deployment and validation."""
    return JsonResponse({'status': 'healthy', 'service': 'SkillBridge', 'version': '1.0.0'})

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def custom_403(request, exception=None):
    return render(request, '403.html', status=403)

def custom_500(request):
    return render(request, '500.html', status=500)
