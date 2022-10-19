# Generated by Django 3.2.9 on 2022-01-12 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_management', '0011_alter_jobassign_transfered_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobassign',
            name='transfered_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_transferred_from', to=settings.AUTH_USER_MODEL, verbose_name='job_transferred_from'),
        ),
    ]