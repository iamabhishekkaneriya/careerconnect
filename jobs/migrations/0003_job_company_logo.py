# Generated by Django 5.1.6 on 2025-02-26 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0002_remove_job_updated_at_job_deadline_job_job_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="company_logo",
            field=models.ImageField(blank=True, null=True, upload_to="company_logos/"),
        ),
    ]
