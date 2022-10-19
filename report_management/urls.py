from django.urls import path
from . import views

urlpatterns = [                                                       
    path('alarm_reponses/<int:pk>/', views.alarm_reponse_report, name="alarm_reponse_report"),                                                                                                                         
    path('employee-travel-log/<int:pk>/', views.emp_travel_log, name="emp_travel_log"),
    path('fetch_emp_route_activity/', views.fetchEmpRouteActivity.as_view(), name="fetch_emp_route_activity"), 
    path('employee_table/', views.employeeTable, name="employee_table"),                                                            
]