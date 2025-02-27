import os
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_file_size(value):
    """Validate file size is under MAX_UPLOAD_SIZE."""
    if value.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(f'File size must be under {settings.MAX_UPLOAD_SIZE/1024/1024}MB')

def validate_file_type(value):
    """Validate file type is allowed."""
    content_type = value.content_type
    if content_type not in settings.CONTENT_TYPES:
        raise ValidationError('File type not supported. Please upload a PDF file.')

def get_resume_path(instance, filename):
    """Generate file path for resume uploads."""
    ext = filename.split('.')[-1]
    filename = f"{instance.college_id}_resume.{ext}"
    return os.path.join('resumes', filename)

def get_avatar_path(instance, filename):
    """Generate file path for avatar uploads."""
    ext = filename.split('.')[-1]
    filename = f"{instance.college_id}_avatar.{ext}"
    return os.path.join('avatars', filename) 