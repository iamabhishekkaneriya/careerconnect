from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import Job, JobApplication
from accounts.models import User

def home(request):
    recent_jobs = Job.objects.filter(status='active').order_by('-created_at')[:6]
    total_jobs = Job.objects.filter(status='active').count()
    total_placements = JobApplication.objects.filter(status='accepted').count()
    
    context = {
        'recent_jobs': recent_jobs,
        'total_jobs': total_jobs,
        'total_placements': total_placements,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

@login_required
def dashboard(request):
    # For students
    applications = JobApplication.objects.filter(student=request.user)
    total_applications = applications.count()
    pending_applications = applications.filter(status='applied').count()
    interview_applications = applications.filter(status='interview_scheduled').count()
    accepted_applications = applications.filter(status='accepted').count()
    recent_applications = applications.order_by('-applied_at')[:5]
    
    # Get recommended jobs (simple example - you might want to implement more sophisticated recommendation logic)
    recommended_jobs = Job.objects.filter(status='active').exclude(
        id__in=applications.values_list('job_id', flat=True)
    ).order_by('-created_at')[:5]
    
    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'interview_applications': interview_applications,
        'accepted_applications': accepted_applications,
        'recent_applications': recent_applications,
        'recommended_jobs': recommended_jobs,
    }
    return render(request, 'core/student_dashboard.html', context)

def calculate_profile_completion(user):
    """Calculate the profile completion percentage for a user."""
    total_fields = 6  # Total number of important profile fields
    completed_fields = 0
    
    if user.first_name and user.last_name:
        completed_fields += 1
    if user.email:
        completed_fields += 1
    if user.phone_number:
        completed_fields += 1
    if user.branch:
        completed_fields += 1
    if user.cgpa:
        completed_fields += 1
    if user.skills:
        completed_fields += 1
    
    return int((completed_fields / total_fields) * 100) 