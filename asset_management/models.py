from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from dashboard.models import AppLog

# Create your models here.



class Asset(models.Model):
    car_name        = models.CharField(max_length=100)
    car_model       = models.CharField(max_length=100, blank=True)
    plate_number    = models.CharField(max_length=100) 
    car_image       = models.ImageField(upload_to='images/car_image', blank=True,null=True)
    is_available    = models.BooleanField(default=True)
    updated_on      = models.DateTimeField(auto_now= True)
    created_on      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.car_name

class AssetAssign(models.Model):
    employee        = models.ForeignKey(User, unique=False, null=True, verbose_name='employee_asset', related_name='employee_asset', on_delete=models.SET_NULL)
    asset           = models.ForeignKey(Asset, unique=False, null=True, verbose_name='asset', related_name='asset', on_delete=models.SET_NULL)
    updated_on      = models.DateTimeField(auto_now= True)
    created_on      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee.username



# Asset Logs
@receiver(post_save, sender=Asset)
def create_asset_save(sender, instance, created, **kwargs):
    asset = instance
    if created:
        app_log             = AppLog()
        app_log.log_type    = "Save"
        app_log.description = f"Asset - {asset.car_name} | Plate No - {asset.plate_number} Saved"
        app_log.log_model   = "Asset"
        app_log.log_url     = "assets/view-assets/"
        app_log.save()

@receiver(pre_delete, sender=Asset)
def delete_asset_signal(sender, instance, **kwargs):
    asset = instance
    app_log             = AppLog()
    app_log.log_type    = "Delete"
    app_log.description = f"Asset - {asset.car_name} | Plate No - {asset.plate_number} Deleted"
    app_log.log_model   = "Asset"
    app_log.log_url     = "assets/view-assets/"
    app_log.save()
