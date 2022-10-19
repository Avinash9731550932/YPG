from import_export import resources
from .models import ETLog

class ETLogResource(resources.ModelResource):
    class Meta:
        model = ETLog
        exclude = ('id',)
        import_id_fields = ('employee', 'asset', 'lat', 'lng', 'city', 'status', 'created_at')