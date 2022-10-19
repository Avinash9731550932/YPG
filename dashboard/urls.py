from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_dashboard, name="view_dashboard"),
    path('change-admin-password', views.change_admin_password, name="change_admin_password"),
    path('logs/view-activity-logs', views.view_activity_logs, name="view_activity_logs")
                                                                   
]