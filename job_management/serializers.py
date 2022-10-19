from rest_framework import serializers

# Models
from accounts.models import ETLog, EmployeeLoginLog


class ETLogSerializer(serializers.Serializer):
    id          =  serializers.CharField(max_length=20) 
    employee_id    =  serializers.CharField(max_length=20)
    # asset_id    =  serializers.CharField(max_length=20)
    username    =  serializers.CharField(max_length=150) 
    lat         =  serializers.DecimalField(max_digits=13, decimal_places=10)
    lng         =  serializers.DecimalField(max_digits=13, decimal_places=10)
    # city        =  serializers.CharField(max_length=256)
    emp_status      =  serializers.CharField(max_length=20) 
    created_at  =  serializers.DateTimeField()