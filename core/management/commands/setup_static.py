from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil

class Command(BaseCommand):
    help = 'Sets up initial static files and directories'

    def handle(self, *args, **kwargs):
        # Create static directories if they don't exist
        static_dirs = [
            'static/css',
            'static/js',
            'static/images',
            'media/resumes',
            'media/avatars',
        ]

        for directory in static_dirs:
            path = os.path.join(settings.BASE_DIR, directory)
            if not os.path.exists(path):
                os.makedirs(path)
                self.stdout.write(
                    self.style.SUCCESS(f'Created directory: {directory}')
                )

        # Create placeholder images
        placeholder_images = {
            'static/images/logo.png': 'CareerConnect logo',
            'static/images/default-avatar.png': 'Default user avatar',
            'static/images/hero-bg.jpg': 'Hero section background',
            'static/images/no-data.svg': 'No data illustration',
            'static/images/no-jobs.svg': 'No jobs illustration',
            'static/images/no-applications.svg': 'No applications illustration',
        }

        for image_path, description in placeholder_images.items():
            path = os.path.join(settings.BASE_DIR, image_path)
            if not os.path.exists(path):
                # Create a simple placeholder image
                with open(path, 'w') as f:
                    f.write(f'# Placeholder for {description}')
                self.stdout.write(
                    self.style.SUCCESS(f'Created placeholder: {image_path}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully set up static files')
        ) 