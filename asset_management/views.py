from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Asset
from .forms import AssetForm
from django.http.response import HttpResponse
import json 


def check_admin(user):
   return user.is_superuser


@user_passes_test(check_admin)
def view_assets(request):
    assets = Asset.objects.all()
    context ={
        'assets' :assets
    }
    return render(request, 'asset_management/view_assets.html', context)


@user_passes_test(check_admin)
def delete_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    asset.delete()
    messages.success(request,'Asset '+ asset.car_name +' has been Deleted')
    return redirect('view_assets')


@user_passes_test(check_admin)
def add_asset(request):
    if request.method == "POST":
        assetform =  AssetForm(request.POST, request.FILES)
        
        if assetform.is_valid():
            assetform.save()
            messages.success(request,'Asset has been updated')
            return redirect('add_asset')
    else:
        assetform = AssetForm()
      
    context ={
        'form' :assetform,
    }
    return render(request, 'asset_management/add_asset.html', context)


@user_passes_test(check_admin)
def update_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        assetform =  AssetForm(request.POST, request.FILES, instance=asset)

        if assetform.is_valid():
            assetform.save()
            messages.success(request,'Asset has been updated')
            return redirect('update_asset', pk=pk)
    else:
        assetform = AssetForm(instance=asset)

    context ={
        'form' :assetform,
        'pk':pk,
    }

    return render(request, 'asset_management/update_asset.html', context)

@user_passes_test(check_admin)
def change_asset_status(request):
    if request.method == "POST":
        asset_id   = request.POST['asset_id']
        status     = request.POST['status']
        asset = get_object_or_404(Asset, pk=asset_id)
        s= True
        if status == '1':
            s= True
        else:
            s= False

        asset.is_available = s
        asset.save()
        return HttpResponse(json.dumps({'status': "success" }), content_type="application/json")

    assets = Asset.objects.all().order_by('car_name')
    context ={
        'assets' :assets
    }
    return render(request, 'asset_management/change_asset_status.html', context)



    

    
