from django.urls import path
from . import views

urlpatterns = [
                                                         
    path('add-asset/', views.add_asset, name="add_asset"),                                                               
    path('view-assets/', views.view_assets, name="view_assets"),  
    path('delete-asset/<int:pk>/', views.delete_asset, name="delete_asset"),  
    path('update-asset/<int:pk>/', views.update_asset, name="update_asset"),  
    path('change-asset-status/', views.change_asset_status, name="change_asset_status"),  
]