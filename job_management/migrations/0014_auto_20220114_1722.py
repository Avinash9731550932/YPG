# Generated by Django 3.2.9 on 2022-01-14 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_management', '0013_auto_20220113_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobreport',
            name='time_off',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='jobreport',
            name='time_on',
            field=models.TimeField(),
        ),
    ]
