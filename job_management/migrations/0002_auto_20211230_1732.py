# Generated by Django 3.2.9 on 2021-12-30 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='employee',
        ),
        migrations.CreateModel(
            name='JobAssign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_type', models.CharField(choices=[('Auto', 'Auto'), ('Manual', 'Manual'), ('Transfer', 'Transfer')], default='Auto', max_length=15)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='employee_job', to=settings.AUTH_USER_MODEL, verbose_name='employee_job')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_assign', to='job_management.job', verbose_name='job_assign')),
                ('transfered_from', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_transferred_from', to=settings.AUTH_USER_MODEL, verbose_name='job_transferred_from')),
            ],
        ),
    ]
