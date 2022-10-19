from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from accounts.models import EmployeeProfile, EmployeeLoginLog
from django.contrib.auth.models import User

# Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from .serializers import EmployeeLoginLogSerializer

import datetime


def check_admin(user):
   return user.is_superuser

@user_passes_test(check_admin)
def view_employee_attendance(request):
    employees = EmployeeProfile.objects.all()

    context ={
        'employees' :employees
    }

    return render(request, 'attendance/view_employee.html', context)

@user_passes_test(check_admin)
def report_detail(request, pk):
    employee = get_object_or_404(User, pk=pk)
    employee_logs = EmployeeLoginLog.objects.filter(employee=employee).order_by('-login_time')
    context={
        "employee_first_name" : employee.first_name,
        "employee_last_name" : employee.last_name,
        "employee_logs": employee_logs,
        "pk":employee.pk
    }
    return render(request, 'attendance/report_detail.html', context)

class fetchEmployeeLoginLogs(APIView):
    def post(self, request, format=None):
        data = request.POST
        employee_id = data.get('employee_id', None)
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)

        start_datef = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_datef = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        end_datef = end_datef + datetime.timedelta(1)
        

        # datefstart = datetime.datetime.combine(start_datef, datetime.time())
        # datefend = datetime.datetime.combine(end_datef, datetime.time())
        # print(datefstart)

        
        loginlogs = EmployeeLoginLog.objects.filter(employee_id = employee_id, login_time__lte=end_datef, login_time__gte=start_datef).order_by('-login_time')
        serializer = EmployeeLoginLogSerializer(loginlogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

