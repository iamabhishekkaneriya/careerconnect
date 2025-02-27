from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, StudentProfile

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False

class StudentAdmin(UserAdmin):
    inlines = (StudentProfileInline,)
    list_display = ('college_id', 'first_name', 'last_name', 'email', 'branch', 'year_of_study', 'cgpa')
    search_fields = ('college_id', 'first_name', 'last_name', 'email')
    ordering = ('college_id',)

    fieldsets = (
        (None, {'fields': ('college_id', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Academic info', {'fields': ('branch', 'year_of_study', 'cgpa', 'skills')}),
        ('Documents', {'fields': ('resume',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('college_id', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(Student, StudentAdmin)