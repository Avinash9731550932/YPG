from django.db import models

# Create your models here.

class CompanyProfile(models.Model):
    company_name        = models.CharField(max_length=30)
    company_logo        = models.ImageField(blank=True, upload_to='images/company', null=True)
    company_address     = models.TextField(blank=True, null=True,default=None)

    
    def __str__(self):
        return self.company_name


class AppLog(models.Model):
    log_type        = models.CharField(max_length=30, blank=True)
    description     = models.CharField(max_length=256, blank=True)
    log_url         = models.CharField(max_length=150, blank=True)
    log_model       = models.CharField(max_length=100, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True, blank=True)
    updated_on      = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.description

