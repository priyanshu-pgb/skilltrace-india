from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, ProfileForm
from .models import User, Profile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_router')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Welcome to SOPAN, {user.first_name or user.username}! Your account has been created.")
            login(request, user)
            if user.is_admin_role:
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
        else:
            messages.error(request, "Please correct the errors below to register.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_router')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_admin_role:
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        name = request.user.first_name or request.user.username
        logout(request)
        messages.info(request, f"You have been safely logged out. Goodbye, {name}!")
    return redirect('landing')


@login_required
def dashboard_router(request):
    """Routes the user to either the admin analytics dashboard or candidate dashboard based on role."""
    if request.user.is_admin_role:
        return redirect('admin_dashboard')
    return redirect('user_dashboard')


@login_required
def profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile information has been successfully updated!")
            return redirect('profile')
        else:
            messages.error(request, "Please review the form errors below.")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileForm(instance=profile)

    context = {
        'user_form': u_form,
        'profile_form': p_form,
        'profile': profile,
    }
    return render(request, 'user/profile.html', context)
