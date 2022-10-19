from django.db import models
from django.contrib.auth.models import User
import os
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

from .signals import *
import datetime

# Create your models here.

from asset_management.models import Asset
from dashboard.models import AppLog

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


STATUS =(
    ('idle', 'idle'),
    ('job_assigned', 'job_assigned'),
    ('inactive', 'inactive'),
)

class EmployeeProfile(models.Model):
    employee            = models.OneToOneField(User, primary_key=True, verbose_name='employee', related_name='employee', on_delete=models.CASCADE)
    profile_picture     = models.ImageField(blank=True, upload_to='images/employee', null=True)
    document_image      = models.ImageField(blank=True, upload_to='images/employee_document', null=True)
    address             = models.TextField(blank=True, null=True,default=None)
    phone_number        = models.CharField(max_length=20,blank=True, null=True, default=None)
    driving_license     = models.CharField(max_length=30,blank=True, null=True, default=None)
    security_license    = models.CharField(max_length=30,blank=True, null=True, default=None)
    status              =  models.CharField(max_length=20, choices=STATUS, default='inactive') 
    
    def __str__(self):
        return force_text(self.employee.username)
    
    
    def filename(self):
        return os.path.basename(self.profile_picture.name)
    
    
    class Meta():
        db_table = 'employee_profile'

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class EmployeeLoginLog(models.Model):
    employee    = models.ForeignKey(User, unique=False, verbose_name='employee_login_logs', related_name='employee_login_logs', on_delete=models.CASCADE)
    login_time  = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    logout_cause = models.CharField(max_length=25,blank=True, null=True, default=None)

    def __str__(self):
        return force_text(self.employee.username)

    @property
    def get_login_time(self):
        login_time = self.login_time + datetime.timedelta(hours=5, minutes=30)
        return login_time.strftime("%I:%M %p")

    @property
    def get_logout_time(self):
        if self.logout_time is None:
            return None
        else:
            logout_time = self.logout_time + datetime.timedelta(hours=5, minutes=30)
            return logout_time.strftime("%I:%M %p")

# EmployeeLoginLog
@receiver(post_save, sender=EmployeeLoginLog)
def create_userlogin_log(sender, instance, created, **kwargs):
    employee_obj = instance
    if created:
        app_log             = AppLog()
        app_log.log_type    = "Save"
        app_log.description = f"Employee {employee_obj.employee.username} Logged in"
        app_log.log_model   = "EmployeeLoginLog"
        app_log.log_url     = "attendance/view-employee-attendance/"
        app_log.save()


        
class ETLog(models.Model):

    STATUS =(
        ('idle', 'idle'),
        ('job_assigned', 'job_assigned'),
    )

    employee    =  models.ForeignKey(User, unique=False, verbose_name='etlog', related_name='etlog', on_delete=models.CASCADE)
    asset       =  models.ForeignKey(Asset, unique=False, verbose_name='etlog_asset', related_name='etlog_asset',blank=True, null=True, on_delete=models.CASCADE)
    lat         =  models.DecimalField(max_digits=13, decimal_places=10, blank=True, null=True, default=None)
    lng         =  models.DecimalField(max_digits=13, decimal_places=10, blank=True, null=True, default=None)
    city        =  models.CharField(max_length=256,blank=True, null=True, default=None)
    login_id    =  models.IntegerField(blank=True, null=True, default=0)
    status      =  models.CharField(max_length=20, choices=STATUS, default='idle') 
    created_at  =  models.DateTimeField(auto_now_add=True)