from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from dashboard.models import AppLog


class Job(models.Model):
    STATUS =(
        ('Created', 'Created'),
        ('Assigned', 'Assigned'),
        ('Cancelled', 'Cancelled'),
        ('Transferred', 'Transferred'),
        ('Completed', 'Completed'),
    )

    job_no              =  models.CharField(max_length=200,blank=False)
    client_name         =  models.CharField(max_length=200,blank=True)
    client_phone_number =  models.CharField(max_length=15,blank=True)
    lat                 =  models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default=None)
    lng                 =  models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default=None)
    address             =  models.CharField(max_length=256,blank=True, null=True, default=None)
    remark              =  models.CharField(max_length=256,blank=True, null=True, default=None)
    zone                =  models.CharField(max_length=256,blank=True, null=True, default=None)
    status              =  models.CharField(max_length=20, choices=STATUS, default='Created') 
    created_at          =  models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.job_no


class JobRequest(models.Model):
    TYPES =(
        ('Auto', 'Auto'),
        ('Manual', 'Manual'),
    )

    job          =  models.ForeignKey(Job, unique=False, verbose_name='job_request', related_name='job_request', on_delete=models.CASCADE)
    employee     =  models.ForeignKey(User, unique=False, verbose_name='employee_job_request', related_name='employee_job_request', on_delete=models.CASCADE)
    request_type =  models.CharField(max_length=20, choices=TYPES, default='Auto') 
    created_at   =  models.DateTimeField(auto_now_add=True)
    updated_on   =  models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.job.job_no


class JobAssign(models.Model):
    TYPES =(
        ('Auto', 'Auto'),
        ('Manual', 'Manual'),
        ('Transfer', 'Transfer'),                   
    )

    job             =  models.ForeignKey(Job, unique=False, verbose_name='job_assign', related_name='job_assign', on_delete=models.CASCADE)
    employee        =  models.ForeignKey(User, unique=False, verbose_name='employee_job', related_name='employee_job', on_delete=models.CASCADE)
    assigned_type   =  models.CharField(max_length=15, choices=TYPES, default='Auto')
    transfered_from =  models.ForeignKey(User, unique=False, blank=True,null=True, verbose_name='job_transferred_from', related_name='job_transferred_from', on_delete=models.CASCADE)
    updated_on      =  models.DateTimeField(auto_now= True)
    created_at      =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job.job_no

class JobReport(models.Model):
    job             =  models.OneToOneField(Job, verbose_name='job_report', related_name='job_report', on_delete=models.CASCADE)
    employee        =  models.ForeignKey(User, unique=False, verbose_name='employee_job_report', related_name='employee_job_report', on_delete=models.CASCADE)
    attendance_note =  models.TextField(max_length=500, blank=True)
    time_on         =  models.TimeField()
    time_off        =  models.TimeField()
    bureu           =  models.CharField(max_length=256,blank=True, null=True, default=None)
    description     =  models.TextField(max_length=500, blank=True)
    created_at      =  models.DateTimeField(auto_now_add=True)
    updated_on      =  models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.job.job_no

class JobReportImage(models.Model):
    job_report  =  models.ForeignKey(JobReport, unique=False, on_delete=models.CASCADE)
    image       =  models.ImageField(upload_to='images/job_report_images/', max_length=500, blank=True, null=True)

    def __str__(self):
        return self.job_report.job.job_no


# Jobs Logs
@receiver(post_save, sender=Job)
def create_job_save(sender, instance, created, **kwargs):
    job = instance
    if created:
        app_log             = AppLog()
        app_log.log_type    = "Save"
        app_log.description = f"Job - {job.job_no} | Client Name - {job.client_name} Saved"
        app_log.log_model   = "Job"
        app_log.log_url     = "jobs/view-jobs/"
        app_log.save()
  

@receiver(pre_delete, sender=Job)
def delete_job_signal(sender, instance, **kwargs):
    job = instance
    app_log             = AppLog()
    app_log.log_type    = "Delete"
    app_log.description = f"Job - {job.job_no} | Client Name - {job.client_name} Deleted"
    app_log.log_model   = "Job"
    app_log.log_url     = "jobs/view-jobs/"
    app_log.save()



@receiver(post_save, sender=JobAssign)
def create_job_assigned_log(sender, instance, created, **kwargs):
    job_assign = instance
    if created:
        app_log             = AppLog()
        app_log.log_type    = "Save"
        app_log.description = f"Job - {job_assign.job.job_no} | Aceepted By - {job_assign.employee.username}"
        app_log.log_model   = "JobAssign"
        app_log.log_url     = "jobs/view-job-assigned-logs/"
        app_log.save()