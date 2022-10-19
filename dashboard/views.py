from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages, auth
from django.contrib.auth.models import User
import datetime

from job_management.models import Job, JobReport
from asset_management.models import Asset
from accounts.models import EmployeeProfile
from .models import AppLog

from django.db.models.functions import Extract
from django.db.models import Count


# Create your views here.

def check_admin(user):
   return user.is_superuser


@user_passes_test(check_admin)
def view_dashboard(request):
    jobs        = Job.objects.all().order_by('-created_at')[:10]
    job_count   = Job.objects.all().count()
    asset_count = Asset.objects.all().count()
    emp_count   = EmployeeProfile.objects.all().count()
    today = datetime.datetime.now()

    job_chart_list  = Job.objects.annotate(month=Extract('created_at', 'month')).values('month').annotate(c=Count('id')).filter(created_at__year=today.year).order_by('month')
    alarm_responses = JobReport.objects.annotate(month=Extract('created_at', 'month')).values('month').annotate(c=Count('id')).filter(created_at__year=today.year).order_by('month')
    
    print(job_chart_list)
    print(alarm_responses)
    context={
       "jobs": jobs,
       "asset_count" :asset_count,
       "emp_count" :emp_count,
       "job_count" :job_count,
       "alarm_responses" : alarm_responses,
       "job_chart_list" : job_chart_list
    }
    return render(request, 'dashboard/index.html', context)

@user_passes_test(check_admin)
def change_admin_password(request):
   if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)

            if success:
                user.set_password(new_password)
                user.save()  # By default Django logs out
                # auth.logout(request)
                messages.success(request, 'Password Updated Successfully!')
                return redirect('change_admin_password')
            else:
                messages.error(request, 'Please Enter Valid Current Password')
                return redirect('change_admin_password')
        else:
            messages.error(request, 'Confirm and New Passwords are not Matching')
            return redirect('change_admin_password')

   return render(request, 'dashboard/change_admin_password.html')

@user_passes_test(check_admin)
def view_activity_logs(request):
    app_logs =AppLog.objects.all().order_by("-created_at")[:150]
    context={
       "app_logs": app_logs,
    }
    return render(request, 'dashboard/view_activity_logs.html', context)

