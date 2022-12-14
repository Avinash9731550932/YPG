# Generated by Django 3.2.9 on 2022-02-10 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asset_management', '0007_auto_20211229_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetassign',
            name='asset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asset', to='asset_management.asset', verbose_name='asset'),
        ),
        migrations.AlterField(
            model_name='assetassign',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee_asset', to=settings.AUTH_USER_MODEL, verbose_name='employee_asset'),
        ),
    ]
