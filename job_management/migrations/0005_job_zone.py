# Generated by Django 3.2.9 on 2022-01-07 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_management', '0004_rename_job_name_job_job_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='zone',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]
