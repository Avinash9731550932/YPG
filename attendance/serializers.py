from rest_framework import serializers


from accounts.models import EmployeeLoginLog

class EmployeeLoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLoginLog
        fields = ['id','login_time', 'logout_time']

