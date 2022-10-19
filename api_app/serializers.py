from rest_framework import serializers

# Models
from asset_management.models import Asset
from accounts.models import EmployeeLoginLog
from job_management.models import Job 


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'car_name', 'car_model', 'plate_number', 'car_image','is_available']


class EmployeeLoginLogSerializer(serializers.ModelSerializer):
    f_login  = serializers.ReadOnlyField(source='get_login_time')
    f_logout = serializers.ReadOnlyField(source='get_logout_time')
    
    class Meta:
        model = EmployeeLoginLog
        fields = ['id','login_time', 'logout_time','logout_cause','f_login','f_logout']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"