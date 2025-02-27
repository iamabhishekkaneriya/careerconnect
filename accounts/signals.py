from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, StudentProfile

@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(student=instance)

@receiver(post_save, sender=Student)
def save_student_profile(sender, instance, **kwargs):
    instance.profile.save() 