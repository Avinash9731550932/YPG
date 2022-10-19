from django.urls import path
from . import views


urlpatterns = [
    path('view-employee-attendance/', views.view_employee_attendance, name="view_employee_attendance"),  
    path('report-detail/<int:pk>/', views.report_detail, name="report_detail"),  
    path('fetch_employee_login_logs/', views.fetchEmployeeLoginLogs.as_view(), name="fetch_employee_login_logs"), 
]