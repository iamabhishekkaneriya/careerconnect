from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Student(AbstractUser):
    email = models.EmailField(unique=True)
    college_id = models.CharField(
        max_length=20, 
        unique=True,
        validators=[RegexValidator(
            regex=r'^[0-9]{2}[A-Z]{3}[0-9]{3}$',
            message='College ID must be in format: 20CSE001'
        )]
    )
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    branch = models.CharField(max_length=50, blank=True)
    year_of_study = models.IntegerField(choices=[
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year')
    ], null=True)
    cgpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True
    )
    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)
    
    # Use college_id for authentication instead of username
    USERNAME_FIELD = 'college_id'
    REQUIRED_FIELDS = ["username",'email']

    def __str__(self):
        return f"{self.college_id} - {self.get_full_name()}"

# Add User as an alias for Student
User = Student

class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    projects = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    achievements = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.student.college_id}"