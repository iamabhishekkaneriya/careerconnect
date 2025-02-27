from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.student_login, name='login'),
    path('logout/', views.student_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
] 