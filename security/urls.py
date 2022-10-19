from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "YPG Security Connectia Administration"
admin.site.site_title = "YPG Security Connectia"
admin.site.index_title = "Welcome to YPG Security Connectia"

urlpatterns = [
    path('connectia/', admin.site.urls),
    path('', include('dashboard.urls')),

    # DRF url
    path('api-auth/', include('rest_framework.urls')),


    path('accounts/', include('accounts.urls')),
    path('assets/', include('asset_management.urls')),
    path('jobs/', include('job_management.urls')),
    path('attendance/', include('attendance.urls')),
    path('support/', include('support_management.urls')),
    path('reports/', include('report_management.urls')),


    path('api/', include('api_app.urls')),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
