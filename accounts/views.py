from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import user_passes_test
from .forms import EmployeeForm, EmployeeProfileForm, UpdateEmployeeForm
from .models import EmployeeProfile
from django.contrib.auth.models import User
from django.conf import settings


def check_admin(user):
   return user.is_superuser


def admin_login(request):
    if request.method == "POST":
         username            = request.POST["username"]
         userpassword        = request.POST["userpassword"]
         user = auth.authenticate(username=username, password=userpassword, is_superuser= True)


         if user is not None and user.is_superuser == True:
            auth_login(request, user)
            messages.success(request,'Successfully Authenticated') 
            return redirect("/")
         else:
             messages.error(request,'Invalid Username or Password') 
    
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')
    else:
        return redirect('/')

@user_passes_test(check_admin)
def admin_logout(request):
    auth.logout(request)
    messages.success(request, 'Your Logged Out!') 
    return redirect('admin_login')

@user_passes_test(check_admin)
def add_employee(request):

    if request.method == "POST":
        employee_form = EmployeeForm(request.POST)
        profile_form =  EmployeeProfileForm(request.POST, request.FILES)
        
        if employee_form.is_valid() and profile_form.is_valid():
            employee = employee_form.save(commit=False)
            employee.set_password(employee_form.cleaned_data['password1'])
            employee.save()
            employee_form.save_m2m()
            
            employee_profile=profile_form.save(commit=False)
            employee_profile.employee = employee
            employee_profile.save()
            profile_form.save_m2m()


            messages.success(request,'Your Profile has been updated')
            return redirect('add_employee')
        else:
            print(employee_form.errors)
            print(profile_form.errors)
    
    else:
        employee_form = EmployeeForm()
        profile_form = EmployeeProfileForm()

    context ={
        'form' :employee_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/add_employee.html', context)

@user_passes_test(check_admin)
def view_employee(request):
    employees = EmployeeProfile.objects.all()

    context ={
        'employees' :employees
    }

    return render(request, 'accounts/view_employee.html', context)

@user_passes_test(check_admin)
def delete_employee(request, pk):
    employee = get_object_or_404(User, pk=pk)
    employee.delete()
    messages.success(request,'Employee has been Deleted')
    return redirect('view_employee')


@user_passes_test(check_admin)
def update_employee(request, pk):
    employee         = get_object_or_404(User, pk=pk)
    employee_profile = get_object_or_404(EmployeeProfile, employee=employee)

    if request.method == "POST":
        employee_form = UpdateEmployeeForm(request.POST, instance=employee)
        profile_form =  EmployeeProfileForm(request.POST, request.FILES, instance=employee_profile)

        if employee_form.is_valid() and profile_form.is_valid():
            employee_form.save()
            profile_form.save()
            messages.success(request,'Employee Data has been updated')
            return redirect('update_employee', pk=pk)

    else:
        
        employee_form = UpdateEmployeeForm(instance=employee)
        profile_form  = EmployeeProfileForm(instance=employee_profile)

    context ={
        'form' :employee_form,
        'profile_form': profile_form,
        'pk':pk,
    }

    return render(request, 'accounts/update_employee.html', context)

@user_passes_test(check_admin)
def view_employee_profile(request, pk):
    employee = get_object_or_404(User, pk=pk)
    context ={
        'employee' :employee,
    }

    return render(request, 'accounts/view_employee_profile.html', context)



@user_passes_test(check_admin)
def change_employee_password(request, pk):
    employee = get_object_or_404(User, pk=pk)
    if request.method == "POST":
      
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if len(new_password) <= 5 or len(confirm_password) <= 5:
            messages.error(request, 'Password should be more than 6 characters')
            return redirect('change_employee_password', pk)

        if new_password == confirm_password:

            employee.set_password(new_password)
            employee.save()

            messages.success(request, 'Password Updated Successfully!')
            return redirect('change_employee_password', pk)
           
        else:
            messages.error(request, 'Confirm and New Passwords are not Matching')
            return redirect('change_employee_password', pk)

    context ={
        'employee' :employee,
    }

    return render(request, 'accounts/change_employee_password.html', context)


@user_passes_test(check_admin)
def company_profile(request):
    # employee = get_object_or_404(User, pk=pk)
    # context ={
    #     'employee' :employee,
    # }

    return HttpResponse("company profile")

@user_passes_test(check_admin)
def employee_track(request):
    context = {
        'google_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'accounts/employee_track.html', context)
