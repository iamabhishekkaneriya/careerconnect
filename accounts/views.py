from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import StudentLoginForm, StudentProfileForm, StudentForm
from .models import StudentProfile

@ensure_csrf_cookie
def student_login(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
        
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:dashboard')
    else:
        form = StudentLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def student_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('accounts:login')

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(student=request.user)
    
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    try:
        profile = request.user.profile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(student=request.user)
    
    if request.method == 'POST':
        user_form = StudentForm(request.POST, request.FILES, instance=request.user)
        profile_form = StudentProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        user_form = StudentForm(instance=request.user)
        profile_form = StudentProfileForm(instance=profile)
    
    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    }) 