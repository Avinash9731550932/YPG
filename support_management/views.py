from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def chatbox(request):
    employee_lists = User.objects.exclude(is_superuser =True, is_staff=True, is_active=False)
    context = {
        "employee_lists" : employee_lists
    }
    return render(request, 'support_management/chatbox.html', context)
