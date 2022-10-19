from django.urls import path
from . import views

urlpatterns = [                                                       
    path('chatbox/', views.chatbox, name="chatbox"),                                                               
]