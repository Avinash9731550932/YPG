# Generated by Django 3.2.9 on 2021-12-29 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_management', '0005_assetassign'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='is_availabe',
            new_name='is_available',
        ),
    ]
