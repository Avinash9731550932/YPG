from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from dashboard.models import AppLog

# USER
@receiver(post_save, sender=User)
def create_user_log(sender, instance, created, **kwargs):
    employee_obj = instance
    if created:
        app_log             = AppLog()
        app_log.log_type    = "Save"
        app_log.description = f"Employee -  {employee_obj.username} Saved"
        app_log.log_model   = "User"
        app_log.log_url     = f"accounts/view-employee-profile/{employee_obj.id}"
        app_log.save()


@receiver(pre_delete, sender=User)
def delete_user_signal(sender, instance, **kwargs):
    employee_obj = instance
    app_log             = AppLog()
    app_log.log_type    = "Delete"
    app_log.description = f"Employee -  {employee_obj.username} Deleted"
    app_log.log_model   = "User"
    app_log.log_url     = f"accounts/view-employee/"
    app_log.save()
