from django.shortcuts import render,get_object_or_404
from django.contrib import  auth
from django.contrib.auth import login as auth_login
from datetime import datetime

# Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


# Models
from django.contrib.auth.models import User
from asset_management.models import Asset, AssetAssign as AssetBook
from accounts.models import EmployeeLoginLog as EmployeeLoginLogModel
from accounts.models import EmployeeProfile as EmployeeProfileModel
from accounts.models import ETLog as ETLogModel
from job_management.models import Job, JobAssign as JobAssignModel
from job_management.models import JobReport,JobReportImage

# Serializers
from .serializers import *
from job_management.pusher import pusher_client
from django.contrib.auth.models import User


######## ACCOUNTS API ############

class EmployeeCreate(APIView):
    def post(self, request, format=None):
        data = request.POST
        username = data.get('username', None)
        password = data.get('password', None)
        email = data.get('email', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)

        user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password,
                                 first_name = first_name,
                                 last_name = last_name)
                                 
        employee_profile = EmployeeProfileModel()
        employee_profile.employee = user
        employee_profile.save()


        if user is not None:
            message = {
                "detail"      : "User Created Successfully",
                "success"     : True,
            }
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {
                "detail" : "User Not created",
                "success" : False,
            }
        
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

class EmployeeLogin(APIView):
    def post(self, request, format=None):
        data = request.POST
        username = data.get('username', None)
        password = data.get('password', None)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)

            empoloyee_login_log = EmployeeLoginLogModel()
            empoloyee_login_log.employee = user
            empoloyee_login_log.save()

            employee_profile = get_object_or_404(EmployeeProfileModel, employee=user)
            employee_profile.status = "idle"
            employee_profile.save()

            loginid= empoloyee_login_log.id

            token = Token.objects.get(user=user)
            message = {
                "detail"      : "Successfully Logged in",
                "success"     : True,
                "employeeid"  : user.pk,
                "token"       : token.key,
                "loginid"     : loginid,
            }
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {
                "detail" : "Invalid Username / Password  ",
                "success" : False,
            }
        
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)


class EmployeeLogout(APIView):
    def get(self, request, format=None):
        data = request.GET
        employeeid =  data.get('employeeid', None)
        loginid    =  data.get('loginid', None)
        assetid    =  data.get('assetid', None)

        auth.logout(request)

        employee = get_object_or_404(User, pk=employeeid)
        asset    = get_object_or_404(Asset, pk=assetid)

        asset.is_available = True
        asset.save()

        employee_profile = get_object_or_404(EmployeeProfileModel, employee=employee)
        employee_profile.status = "inactive"
        employee_profile.save()

        empoloyee_login_log = EmployeeLoginLogModel.objects.get(pk=loginid)
        empoloyee_login_log.logout_time = datetime.now()
        empoloyee_login_log.logout_cause = "App logout"
        empoloyee_login_log.save()
        
        message = {
            "detail"    : "Successfully logged out",
            "success"   : True,
        }
        return Response(message, status=status.HTTP_200_OK)


class EmployeeProfile(APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self, request, *args, **kwargs):
       pk = self.kwargs['pk']
       user = get_object_or_404(User, pk=pk)

       profile_pic = ""
       document_image = ""
       if user.employee.profile_picture:
           profile_pic = user.employee.profile_picture.url
       if user.employee.document_image:
           document_image = user.employee.document_image.url
       message = {
                "success"           : True,
                "employeeid"        : user.pk,
                "username"          : user.username,
                "email"             : user.email,
                "first_name"        : user.first_name,
                "last_name"         : user.last_name,
                "phone_number"      : user.employee.phone_number,
                "security_license"  : user.employee.security_license,
                "profile_picture"   : profile_pic,
                "document_image"    : document_image,
                "address"           : user.employee.address,
                "driving_license"   : user.employee.driving_license,
            }
       return Response(message, status=status.HTTP_200_OK)

class ChangeEmployeeProfile(APIView):
    permission_classes = (IsAuthenticated,) 
    def post(self, request, format=None):

        employee         = request.user
        employee_profile = get_object_or_404(EmployeeProfileModel, employee=employee)

        data = request.POST

        first_name       =  data.get('first_name', None)
        last_name        =  data.get('last_name', None)
        phone_number     =  data.get('phone_number', None)
        driving_license  =  data.get('driving_license', None)
        security_license =  data.get('security_license', None)
        profile_image    =  request.FILES.getlist('file')

        try:
            employee.first_name = first_name
            employee.last_name  = last_name
            employee.save()
            if employee.pk is not None:
                employee_profile.phone_number     = phone_number
                employee_profile.driving_license  = driving_license
                employee_profile.security_license = security_license
                employee_profile.security_license = security_license
                if profile_image:
                   employee_profile.profile_picture = profile_image
                employee_profile.save() 

                message = {
                    "detail" : "Profile Changed Successfully",
                    "success" : True,
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {
                    "detail" : "Profile not changed",
                    "success" : False,
                }
                return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)

        except:
                message = {
                    "detail" : "Profile not changed",
                    "success" : False,
                }
                return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)

        


class ChangePasswordEmployee(APIView):
     permission_classes = (IsAuthenticated,) 
     def post(self, request, format=None):
        data = request.POST
        employeeid          =  data.get('employeeid', None)
        current_password    =  data.get('current_password', None)
        new_password        =  data.get('new_password', None)
        confirm_password    =  data.get('confirm_password', None)

        if len(new_password) <= 5 or len(confirm_password) <= 5:
            message = {
                "detail" : "Password should be more than 6 characters",
                "success" : False,
            }
            return Response(message, status=status.HTTP_411_LENGTH_REQUIRED)

        user = get_object_or_404(User, pk=employeeid)

        if new_password == confirm_password:
            success = user.check_password(current_password)

            if success:
                user.set_password(new_password)
                user.save() 
                
                message = {
                    "detail" : "Password Changed Successfully",
                    "success" : True,
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {
                    "detail" : "Current Password Not Matched",
                    "success" : False,
                }
                return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
                message = {
                    "detail" : "New Password & Current Password not Matching",
                    "success" : False,
                }
                return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)


class EmployeeLoginLogs(APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        employee = get_object_or_404(User, pk=pk)

        employee_login_logs = EmployeeLoginLogModel.objects.filter(employee=employee).order_by('-login_time')[:10]
        serializer = EmployeeLoginLogSerializer(employee_login_logs, many=True)
        
        message = {
            "detail" : "Logs Fetched",
            "success" : True,
            "logs"  : serializer.data

        }
        return Response(message, status=status.HTTP_200_OK)


class EmployeeLoginLogDetail(APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        employee_login_log = EmployeeLoginLogModel.objects.get(pk=pk)
        serializer = EmployeeLoginLogSerializer(employee_login_log, many=False)
        
        message = {
            "detail" : "Log Fetched",
            "success" : True,
            "log"  : serializer.data
        }

        return Response(message, status=status.HTTP_200_OK)

######## ASSETS API ###########  

class AssetList(APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self, request, format=None):
        assets = Asset.objects.all().order_by('-is_available')
        serializer = AssetSerializer(assets, many=True)

        message = {
            "detail"  : "Assets Fetched",
            "success" : True,
            "asset"   : serializer.data
        }
        return Response(message, status=status.HTTP_200_OK)

class AssetAssign(APIView):
     permission_classes = (IsAuthenticated,) 
     def post(self, request, format=None):
        data = request.POST
        employeeid  =  data.get('employeeid', None)
        assetid     =  data.get('assetid', None)
        employee    =  get_object_or_404(User, pk=employeeid)
        asset       =  get_object_or_404(Asset, pk=assetid)

        try:
            asset.is_available = False
            asset.save()
            asset_assign = AssetBook()
            asset_assign.employee = employee
            asset_assign.asset = asset
            asset_assign.save()
             
            message = {
                "detail" : "Asset Assigned Successfully",
                "success" : True,
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = {
                "detail" : "Asset Not Assigned/ Something Went wrong",
                "success" : False,
            }
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)

class ETLog(APIView):
    permission_classes = (IsAuthenticated,) 
    def post(self, request, format=None):
        data = request.POST
        employeeid  =  data.get('employeeid', None)
        assetid     =  data.get('assetid', None)
        lat         =  data.get('lat', None)
        lng         =  data.get('lng', None)
        city        =  data.get('city', None)
        login_id    =  data.get('login_id', None)
        status_log  =  data.get('status', 'Idle')

        employee    =  get_object_or_404(User, pk=employeeid)
        asset       =  get_object_or_404(Asset, pk=assetid)

        try:
            etlog = ETLogModel()
            etlog.employee  = employee
            etlog.asset     = asset
            etlog.lat       = lat
            etlog.lng       = lng
            etlog.city      = city
            etlog.login_id  = login_id
            etlog.status    = status_log
            etlog.save()
             
            message = {
                "detail" : "ETLog Saved",
                "success" : True,
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = {
                "detail" : e,
                "success" : False,
            }
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)


######## JOB API ##########
class JobDetail(APIView):
    permission_classes = (IsAuthenticated,) 
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        job = get_object_or_404(Job, pk=pk)
        serializer = JobSerializer(job, many=False)
        
        message = {
            "detail" : "job Fetched",
            "success" : True,
            "job"  : serializer.data

        }
        return Response(message, status=status.HTTP_200_OK)

class AlarmResponseReport(APIView):
    permission_classes = (IsAuthenticated,) 
    def post(self, request, format=None):
        data = request.POST
        employeeid      =  data.get('employeeid', None)
        job_id          =  data.get('job_id', None)
        attendance_note =  data.get('attendance_note', None)
        time_on         =  data.get('time_on', None)
        time_off        =  data.get('time_off', None)
        description     =  data.get('description', None)
        bureu           =  data.get('bureu', None)
        images          =  request.FILES.getlist('file_field')

        employee        =  get_object_or_404(User, pk=employeeid)
        job             =  get_object_or_404(Job, pk=job_id)

        try:
            job_report                 = JobReport()
            job_report.employee        = employee
            job_report.job             = job
            job_report.attendance_note = attendance_note
            job_report.time_on         = time_on
            job_report.time_off        = time_off
            job_report.description     = description
            job_report.bureu           = bureu
            job_report.save()
            job.status                 = "Completed"
            job.save()
            employee_profile = get_object_or_404(EmployeeProfileModel, employee=employee)
            employee_profile.status = "idle"
            employee_profile.save()
 
            # Save report Images
            if len(images) > 0 :
                for f in images:
                    job_report_image = JobReportImage()
                    job_report_image.job_report = job_report
                    job_report_image.image = f
                    job_report_image.save()

            message = {
                "detail" : "Alarm response report created Successfully",
                "success" : True,
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = {
                "detail" : f"Not Saved {e}",
                "success" : False,
            }
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)


class JobAssignAPI(APIView):
    permission_classes = (IsAuthenticated,) 
    def post(self, request, format=None):
        data = request.POST
        employeeid    =  data.get('employeeid', None)
        job_id        =  data.get('job_id', None)
      #   assigned_type =  data.get('assigned_type', None)
        employee      =  get_object_or_404(User, pk=employeeid)
        job           =  get_object_or_404(Job, pk=job_id)

        if job.status == "Created" or job.status =="Cancelled":

            try:
                  job_assign               = JobAssignModel()
                  job_assign.employee      = employee
                  job_assign.job           = job
                  # job_assign.assigned_type = assigned_type
                  job_assign.save()
                  job.status  = "Assigned"
                  job.save()

                  employee_profile = get_object_or_404(EmployeeProfileModel, employee=employee)
                  employee_profile.status = "job_assigned"
                  employee_profile.save()

                  # ABORT AUTO JOB REQUEST ASSIGNING
                  global IS_JOB_REQUEST_RUNNING
                  IS_JOB_REQUEST_RUNNING = False
                  
                  message = {
                     "detail" : f"Job Assigned Successfully",
                     "success" : True,
                  }

                  admin_lists = User.objects.filter(is_superuser = True)
                  for admin_list in admin_lists:
                     pusher_client.trigger(f'private-admin{ admin_list.username }-channel', 'job_request_feedback', 
                     {
                        'message': f"Job Request Accepted by {employee.username} ",
                        "type":'success',
                        "job_id": job_id,
                        'job_accepted': "true",
                     })


                  return Response(message, status=status.HTTP_200_OK)
            except Exception as e:
                  message = {
                     "detail" : f"Job Not Assigned/ Something Went wrong {e}",
                     "success" : False,
                  }
                  
                  admin_lists = User.objects.filter(is_superuser = True)
                  for admin_list in admin_lists:
                    pusher_client.trigger(f'private-admin{ admin_list.username }-channel', 'job_request_feedback', 
                    {
                        'message': f"ERROR while Job Request Accept by {employee.username}",
                        "type":'danger',
                        "job_id": job_id

                    })
                  return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
             admin_lists = User.objects.filter(is_superuser = True)
             for admin_list in admin_lists:
                pusher_client.trigger(f'private-admin{ admin_list.username }-channel', 'job_request_feedback', 
                        {
                            'message': f"{employee.username} Tried to accept request, its already assigned",
                            "type":'warning',
                            "job_id": job_id
                        })

             message = {
                        "detail" : f"This Job already assigned to another employee",
                        "success" : False,
                    }
             return Response(message, status=status.HTTP_200_OK)

class JobRequestDenied(APIView):
    permission_classes = (IsAuthenticated,) 
    def post(self, request, format=None):
        data          =  request.POST
        employee      =  request.user
        job_id        =  data.get('job_id', None)
      #   employee      =  get_object_or_404(User, pk=employeeid)
      #   job           =  get_object_or_404(Job, pk=job_id)

        message = {
            "detail" : f"Job request denied Successfully",
            "success" : True,
        }

        admin_lists = User.objects.filter(is_superuser = True)
        for admin_list in admin_lists:
            pusher_client.trigger(f'private-admin{ admin_list.username }-channel', 'job_request_feedback', 
            {
                'message': f"Employee - {employee.username} Denied Job request",
                "type":'danger',
                "job_id": job_id
            })

        return Response(message, status=status.HTTP_200_OK)


class JobCancelled(APIView):
    permission_classes = (IsAuthenticated,) 
    def post(self, request, format=None):
        data          =  request.POST
        employee      =  request.user
        job_id        =  data.get('job_id', None)  
        job           =  get_object_or_404(Job, pk=job_id)

        job.status  = "Cancelled"
        job.save()

        employee_profile = get_object_or_404(EmployeeProfileModel, employee=employee)
        employee_profile.status = "idle"
        employee_profile.save()

        message = {
            "detail" : f"Job Cancelled Successfully",
            "success" : True,
        }

        admin_lists = User.objects.filter(is_superuser = True)
        for admin_list in admin_lists:
            pusher_client.trigger(f'private-admin{ admin_list.username }-channel', 'job_request_feedback', 
            {
                'message': f"Employee - {employee.username} Cancelled Job",
                "type":'danger',
                "job_id": job_id
            })

        return Response(message, status=status.HTTP_200_OK)

