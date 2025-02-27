from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Job, Skill, JobApplication
from .forms import JobForm, JobApplicationForm
from django.core.paginator import Paginator

@login_required
def job_list(request):
    jobs = Job.objects.filter(status='active')
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
    })

@login_required
def job_apply(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if already applied
    if JobApplication.objects.filter(student=request.user, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.job = job
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('jobs:my_applications')
    else:
        form = JobApplicationForm()
    
    return render(request, 'jobs/job_apply.html', {
        'form': form,
        'job': job,
    })

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = JobApplication.objects.filter(student=request.user, job=job).exists()
    print(f"User: {request.user}, Job ID: {job_id}, Job Title: {job.title}, Company: {job.company}, Has Applied: {has_applied}")  # Debug message



    print(f"Job ID: {job.id}, Has Applied: {has_applied}")  # Debug message


    
    if request.method == 'POST' and not has_applied:
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.job = job
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('jobs:my_applications')
    else:
        form = JobApplicationForm()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'form': form,
        'has_applied': has_applied,
    })

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(student=request.user)
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    # Sort applications
    sort = request.GET.get('sort', '-applied_at')  # Default sort by application date
    applications = applications.order_by(sort)
    
    return render(request, 'jobs/my_applications.html', {
        'applications': applications,
        'status_choices': JobApplication.STATUS_CHOICES,
        'current_status': status,
    })

@login_required
def update_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, student=request.user)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application status updated successfully!')
            return redirect('jobs:my_applications')
    else:
        form = JobApplicationForm(instance=application)
    
    return render(request, 'jobs/update_application.html', {
        'form': form,
        'application': application,
    })

@login_required
def withdraw_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, student=request.user)
    
    if request.method == 'POST':
        application.status = 'withdrawn'
        application.save()
        messages.success(request, 'Application withdrawn successfully.')
        return redirect('jobs:my_applications')
    
    return render(request, 'jobs/withdraw_application.html', {
        'application': application,
    })

@login_required
def job_post(request):
    if not request.user.is_employer:
        messages.error(request, 'Only employers can post jobs.')
        return redirect('jobs:job_list')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user
            job.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = JobForm()
    
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'jobs/job_form.html', context)

@login_required
def job_edit(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Security check
    if request.user != job.company:
        messages.error(request, 'You do not have permission to edit this job.')
        return redirect('jobs:job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)
    
    context = {
        'form': form,
        'job': job,
        'is_edit': True,
    }
    return render(request, 'jobs/job_form.html', context)

@login_required
def job_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Security check
    if request.user != job.company:
        messages.error(request, 'You do not have permission to delete this job.')
        return redirect('jobs:job_detail', job_id=job_id)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('jobs:job_list')
    
    context = {
        'job': job,
    }
    return render(request, 'jobs/job_confirm_delete.html', context)

@login_required
def job_manage(request):
    if not request.user.is_employer:
        messages.error(request, 'Only employers can manage jobs.')
        return redirect('jobs:job_list')
    
    jobs = Job.objects.filter(company=request.user).order_by('-created_at')
    
    context = {
        'jobs': jobs,
    }
    return render(request, 'jobs/job_manage.html', context)

@login_required
def update_application_status(request, application_id):
    if not request.user.is_employer:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    application = get_object_or_404(JobApplication, id=application_id)
    
    # Security check
    if request.user != application.job.company:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    new_status = request.POST.get('status')
    if new_status not in dict(JobApplication.STATUS_CHOICES):
        return JsonResponse({'error': 'Invalid status'}, status=400)
    
    application.status = new_status
    application.save()
    
    return JsonResponse({
        'success': True,
        'new_status': application.get_status_display()
    })
