from .models import CompanyProfile, AppLog
from django.conf import settings


def get_company_info(request):
    company_info = CompanyProfile.objects.all().first()
    return {'company_info': company_info}

def get_applog(request):
    app_logs = AppLog.objects.all().order_by('-created_at')[:15]
    context = {
        'app_logs' : app_logs,
        'SITE_URL' : settings.SITE_URL
    }
        
    return context
    