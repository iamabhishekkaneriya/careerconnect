from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Student
import re

class Command(BaseCommand):
    help = 'Create a new student account with ID and password'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str, help='Student ID (Format: 20CSE001)')
        parser.add_argument('password', type=str, help='Password for the student')
        parser.add_argument('--first_name', type=str, help='First name of the student')
        parser.add_argument('--last_name', type=str, help='Last name of the student')
        parser.add_argument('--email', type=str, help='Email of the student')
        parser.add_argument('--force', action='store_true', help='Force update if student exists')

    def handle(self, *args, **options):
        student_id = options['student_id'].upper()  # Convert to uppercase
        password = options['password']
        force = options.get('force', False)
        
        # Validate student ID format
        if not re.match(r'^[0-9]{2}[A-Z]{3}[0-9]{3}$', student_id):
            self.stdout.write(self.style.ERROR('Invalid student ID format. Must be like: 20CSE001'))
            return
        
        try:
            # Check if student already exists (check both username and college_id)
            existing_student = Student.objects.filter(username=student_id).first() or \
                             Student.objects.filter(college_id=student_id).first()
            
            if existing_student:
                if not force:
                    self.stdout.write(self.style.ERROR(
                        f'Student with ID {student_id} already exists. '
                        'Use --force to update the existing account.'
                    ))
                    return
                # Update existing student
                existing_student.username = student_id
                existing_student.college_id = student_id  # Set both fields
                existing_student.set_password(password)
                if options.get('first_name'):
                    existing_student.first_name = options['first_name']
                if options.get('last_name'):
                    existing_student.last_name = options['last_name']
                if options.get('email'):
                    existing_student.email = options['email']
                existing_student.save()
                self.stdout.write(self.style.SUCCESS(f'Updated existing student account: {student_id}'))
            else:
                # Create new student
                student = Student.objects.create_user(
                    username=student_id,
                    college_id=student_id,  # Set both fields
                    password=password,
                    first_name=options.get('first_name', ''),
                    last_name=options.get('last_name', ''),
                    email=options.get('email', '')
                )
                self.stdout.write(self.style.SUCCESS(f'Created new student account: {student_id}'))

            self.stdout.write('Student can now login with:')
            self.stdout.write(f'Student ID: {student_id}')
            self.stdout.write(f'Password: {password}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error managing student account: {str(e)}')) 