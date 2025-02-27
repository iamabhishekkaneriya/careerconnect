from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Job listings and details
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.job_apply, name='job_apply'),
    
    # Application management
    path('my-applications/', views.my_applications, name='my_applications'),
    path('application/<int:application_id>/update/', views.update_application, name='update_application'),
    path('application/<int:application_id>/withdraw/', views.withdraw_application, name='withdraw_application'),
    
    # Job management (for employers)
    path('post/', views.job_post, name='job_post'),
    path('<int:job_id>/edit/', views.job_edit, name='job_edit'),
    path('<int:job_id>/delete/', views.job_delete, name='job_delete'),
    path('manage/', views.job_manage, name='job_manage'),
    
    # Application status management
    path('applications/<int:application_id>/update-status/', views.update_application_status, name='update_application_status'),
] 