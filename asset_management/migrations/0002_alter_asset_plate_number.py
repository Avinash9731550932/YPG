# Generated by Django 3.2.9 on 2021-12-17 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='plate_number',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
