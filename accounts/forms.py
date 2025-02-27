from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from .models import Student, StudentProfile

class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student ID (e.g., 20CSE001)'
            }
        ),
        label='Student ID'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password'
            }
        )
    )

    def clean(self):
        """Convert username to college_id for authentication"""
        cleaned_data = super().clean()
        if 'username' in cleaned_data:
            cleaned_data['username'] = cleaned_data['username'].upper()
        return cleaned_data

    class Meta:
        model = Student
        fields = ['username', 'password']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['student']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'linkedin_profile': forms.URLInput(attrs={'class': 'form-control'}),
            'github_profile': forms.URLInput(attrs={'class': 'form-control'}),
            'projects': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'certifications': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'achievements': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class StudentForm(UserChangeForm):
    password = None  # Remove password field from the form

    class Meta:
        model = Student
        fields = ['profile_photo', 'first_name', 'last_name', 'email', 'phone_number', 
                 'branch', 'year_of_study', 'cgpa', 'skills', 'resume']
        widgets = {
            'profile_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_study': forms.Select(attrs={'class': 'form-control'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        } 