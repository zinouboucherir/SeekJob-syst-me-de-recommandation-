# Generated by Django 3.0.6 on 2022-04-28 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SEEKJOBSPLATFORM', '0003_auto_20220428_0854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seeker_resume',
            old_name='job_education_extracted',
            new_name='cv_education_extracted',
        ),
        migrations.RenameField(
            model_name='seeker_resume',
            old_name='job_experience_extracted',
            new_name='cv_experience_extracted',
        ),
        migrations.RenameField(
            model_name='seeker_resume',
            old_name='job_skills_extracted',
            new_name='cv_skills_extracted',
        ),
    ]
