# Generated by Django 3.2.9 on 2022-01-19 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_management', '0014_auto_20220114_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobreport',
            name='job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_report', to='job_management.job', verbose_name='job_report'),
        ),
    ]