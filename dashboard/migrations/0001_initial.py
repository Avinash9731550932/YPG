# Generated by Django 3.2.9 on 2021-12-28 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='images/company')),
                ('company_address', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
    ]
