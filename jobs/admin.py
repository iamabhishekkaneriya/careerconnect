from django.contrib import admin
from .models import Job, Skill, JobApplication

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'status', 'created_at')
    list_filter = ('status', 'job_type')
    search_fields = ('title', 'company')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('student__username', 'job__title')

admin.site.register(Job, JobAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
