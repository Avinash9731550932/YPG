from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.admin_login, name="admin_login"),                                                               
    path('logout/', views.admin_logout, name="admin_logout"),                                                               
    path('add-employee/', views.add_employee, name="add_employee"),                                                               
    path('view-employee/', views.view_employee, name="view_employee"),  
    path('delete-employee/<int:pk>', views.delete_employee, name="delete_employee"),  
    path('update-employee/<int:pk>', views.update_employee, name="update_employee"),  
    path('view-employee-profile/<int:pk>', views.view_employee_profile, name="view_employee_profile"),
    path('company-profile/', views.company_profile, name="company_profile"),
    path('change-employee-password/<int:pk>', views.change_employee_password, name="change_employee_password"),
    path('employee-track/', views.employee_track, name="employee_track"),
]