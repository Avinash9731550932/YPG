# Generated by Django 3.2.9 on 2022-01-12 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_management', '0006_jobrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='request_type',
            field=models.CharField(choices=[('Auto', 'Auto'), ('Manual', 'Manual')], default='Auto', max_length=20),
        ),
    ]
