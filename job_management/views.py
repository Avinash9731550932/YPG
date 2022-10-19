import logging
import traceback

from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from accounts.models import ETLog
from .models import Job, JobRequest, JobAssign, JobReport
from .serializers import ETLogSerializer

# Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .pusher import pusher_client
import time
import json

from google.cloud.firestore import GeoPoint
from firebase_admin import firestore as fireview

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "ypg-security",
  "private_key_id": "e37de4f6b003d78bf095546469ee59c286ca04da",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCKBE9Xe4R2/t/1\nxANJ+1S5n44B573Z/JOenRAQoqkLcm9w1uFNIlIGNWUWpieRb2hmDtgXpC1cgvwv\n8O0m928bwVDKrgQEjvqaCALCSLdcMEBS60rLQFksTFHCQS+BPdEkDLaqvbxPxVQ6\ngsVefeppcqdL/ePPjeiccZ44U/i4F4OgXWBYZr/V1pwRH8ZHHLI/413qHbkOg2rd\nLUFHL0heiXmcFtC/mNhmIJBoPuNESzlenKWYZynSXXLm2+ldqtz+KedhMAerQpiB\na2dVjmRROpvMpwXAYWVXsO2dTRjGEFX0PzKReTzzb15ib0WT6Bid1qGu4xv5rLCp\nqv4AVZcVAgMBAAECggEAB7iBAGmqTzEn3IA9bNyQm0eyh9HBHETVtI2gZ0XU2Lfr\nRa/c76syqnfp3UVTOP63TjTuCriGScK8En8oTRc8vHE+hfALzSjQb7XGAxH9S+du\nbxUMMeg6H3vE0RiYweKa5KjfaRgZxN6gPRuxUygOaR1fACXGTNyT6CMvpi1bCwqU\nrHmPahpYLaPqiyjtNzOfwXAyy9dym5g1ULKhnxKRAlF2VTcNijsrFdAezEB2uLGL\nmZOsGr+PKdDYfxBtCEiSDn4YpgAlfBMhjKERSzA71y2XR0z2LY0D8ybBL+RzllHO\nbkMLmJTysynI1vX/7llCSGKde+lDH3xj2uk6bKxamwKBgQC8LNxZSa8py9+GDlCL\nsa9Sp8dFtvDiRfCcm7VuPuAmGqf3JMfF3YiMopLuleqthf+8JV7ZsN0fjxZZ5Po1\nnIh5bJ44pSngkdVUwMBiCEb3ZBVDeVOCz9rBfqqoz1l0ZBgNg4t6ZtG0eAExe7Oh\nw6gaOqTUWjiqAdQm5ybKTHC7JwKBgQC7w0cIIOCl/uEWzAsaaE50USgHw6qjG6hy\namQNbdlIQm2bvjEde+Qki5hjtQeTbfN8Wpagwahr2xIlgExqWdQlgrVNOZasgFhC\n2Zaf8NNA4gNdgBSlD6fU1/CEX1LFq+zBbHG4B5wG3M5i2W4scSScsD6xxS0LO/k3\nijq+OXdxYwKBgQCvTOd1sqQgvtGb9CfrC3u196E3e+bKFLfDXXdWnfJ47Oo+3Z/R\n38A+q5FP/I9kWenU38eN6ysEJGuBEURav1mQLLT1NkBd+d2QGAThDq719uGsOxGm\nUnaLPbJEku3V9Q1HQZ2lSLXhds49x+yfLUOkM6+sN+SD1DJMj5hea3m1jwKBgGim\n/wBY0t2yomLCd63QVWofkeBB/unKkKi1A+84OtM7szwLVfTJCPAVnmp0jDRwJDY7\nh5kyV11GTWb5i537U3NU1xij8IdVQdyAyqN650RStO14ZglaIIFRmo0tVEU4/k0Q\n1JFuLFjm2WHfLrk2luF+mnMbI3APjWiXcwZzoU9hAoGADZdvUpHQiZtqBF24u+DS\n/rCbHd3+y8yIKT2d3vKK+qiqsMlCq0i081RAD+Vi0imTZTmwzxElR2hy5IVALd4O\nx53hpCRaNlrCgEpk+sEs8Ivj381PaFKd+LKILzcVlOPG+8jNd6Sp9x7W2aaHWsov\nXMAb2a1bzKugTgo9Bwb2mpI=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-70o1p@ypg-security.iam.gserviceaccount.com",
  "client_id": "115144072705706582837",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-70o1p%40ypg-security.iam.gserviceaccount.com"
})
firebase_app = firebase_admin.initialize_app(cred)

fdatabase = firestore.client(app=firebase_app)

IS_JOB_REQUEST_RUNNING = False


def check_admin(user):
    return user.is_superuser


@user_passes_test(check_admin)
def assign_job(request):
    context = {
        'google_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'job_management/job_assign.html', context)


@user_passes_test(check_admin)
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    context = {
        "job": job,
        'google_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'job_management/job_detail.html', context)


@user_passes_test(check_admin)
def save_job(request):
    if request.method == "POST":
        address = request.POST['address_txt']
        jobno = request.POST['job_no_txt']
        zone = request.POST['job_zone_txt']
        lat = request.POST['lat_txt']
        lng = request.POST['lng_txt']
        client_name = request.POST['client_name_txt']
        client_phone = request.POST['client_phone_txt']
        remark = request.POST['remark_txt']

        job = Job()
        job.job_no = jobno
        job.client_name = client_name
        job.client_phone_number = client_phone
        job.lat = lat
        job.lng = lng
        job.address = address
        job.remark = remark
        job.zone = zone
        job.status = "Created"
        job.save()

        if job.pk is None:
            return HttpResponse(json.dumps({'status': "0"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': "1", 'id': job.pk}), content_type="application/json")


@user_passes_test(check_admin)
def update_job(request):
    if request.method == "POST":
        address = request.POST['address_txt']
        jobno = request.POST['job_no_txt']
        zone = request.POST['job_zone_txt']
        lat = request.POST['lat_txt']
        lng = request.POST['lng_txt']
        client_name = request.POST['client_name_txt']
        client_phone = request.POST['client_phone_txt']
        remark = request.POST['remark_txt']
        job_id = request.POST['job_id_hidden']

        job = get_object_or_404(Job, pk=job_id)
        job.job_no = jobno
        job.client_name = client_name
        job.client_phone_number = client_phone
        job.lat = lat
        job.lng = lng
        job.address = address
        job.remark = remark
        job.zone = zone
        job.save()

        if job.pk is None:
            return HttpResponse(json.dumps({'status': "0"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': "1", 'id': job.pk}), content_type="application/json")


@user_passes_test(check_admin)
def view_jobs(request):
    jobs = Job.objects.all().order_by('-created_at')
    context = {
        "jobs": jobs
    }
    return render(request, 'job_management/view_jobs.html', context)


@user_passes_test(check_admin)
def view_alarm_response(request):
    job_report = JobReport.objects.all().order_by('-created_at')
    context = {
        "job_reports": job_report
    }
    return render(request, 'job_management/view_alarm_response.html', context)


class FetchEmpLive(APIView):
    def get(self, request, format=None):
        etlogs = ETLog.objects.raw(
            "SELECT accounts_etlog.id,accounts_etlog.employee_id, accounts_etlog.created_at, accounts_etlog.lat, accounts_etlog.lng, auth_user.username, employee_profile.status as emp_status FROM public.accounts_etlog INNER JOIN public.auth_user ON accounts_etlog.employee_id=auth_user.id  INNER JOIN public.employee_profile ON employee_profile.employee_id=auth_user.id WHERE  created_at IN (SELECT MAX(created_at) FROM public.accounts_etlog WHERE created_at > current_timestamp - interval '10 minutes' GROUP BY employee_id)")
        etloglist = list(etlogs)
        serializer = ETLogSerializer(etloglist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
def auth_pusher(request):
    auth = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id']
    )
    return JsonResponse(auth)


@user_passes_test(check_admin)
def change_job_request_process(request):
    global IS_JOB_REQUEST_RUNNING
    IS_JOB_REQUEST_RUNNING = False
    return HttpResponse(json.dumps({'status': "success"}), content_type="application/json")


@user_passes_test(check_admin)
def job_pusher_trigger(request):
    job_id = request.POST['job_id']
    job = get_object_or_404(Job, pk=job_id)
    emp_distance = json.loads(request.POST.get('emp_distance', ''))

    # First clear all data in firebase
    # fdatabase.child("alarm_reponse").child().remove()
    docs = fdatabase.collection("JobAlert").get()
    for doc in docs:
        key = doc.id
        fdatabase.collection("JobAlert").document(key).delete()

    # Make Status True
    global IS_JOB_REQUEST_RUNNING
    IS_JOB_REQUEST_RUNNING = True
    for emp in emp_distance:
        if IS_JOB_REQUEST_RUNNING == True:
            print(emp['employee_id'])
            emp_id = emp['employee_id']
            emp_name = emp['username']
            employee = get_object_or_404(User, pk=emp_id)

            job_request = JobRequest()
            job_request.employee = employee
            job_request.job = job
            job_request.request_type = "Auto"
            job_request.save()

            # print(f'private-emp-{emp_id}-channel')
            # pusher_client.trigger(f'private-emp-{emp_id}-channel', 'job_request_trigger',
            # {
            # 'message': job_id
            # })

            data = {
                "job_id": job.id,
                "employee_id": employee.id,
                "job_client_name": job.client_name,
                "job_client_number": job.client_phone_number,
                "job_latlng": GeoPoint(job.lat, job.lng),
                "job_zone": job.zone,
                "job_remarks": job.remark,
                "job_address": job.address,
                "job_no": job.job_no,
                "Accept": "false",
                "created_at": fireview.SERVER_TIMESTAMP
            }
            fdatabase.collection("JobAlert").add(data)

            pusher_client.trigger(f'private-admin{request.user.username}-channel', 'job_request_feedback',
                                  {
                                      'message': f"Job Sent to {emp_name} -- AUTO",
                                      "type": 'success',
                                      "job_id": job_id
                                  })
            time.sleep(30)
        else:
            break

    return HttpResponse(json.dumps({'status': "success"}), content_type="application/json")


@user_passes_test(check_admin)
def job_manual_assign(request):
    try:
        job_id = request.POST['job_id']
        emp_id = request.POST['emp_id']
        emp_id = request.POST['emp_id']
        emp_username = request.POST['emp_username']
        type = request.POST['type']

        job = get_object_or_404(Job, pk=job_id)
        employee = get_object_or_404(User, pk=emp_id)

        # First clear all data in firebase
        # fdatabase.child("alarm_reponse").child().remove()
        docs = fdatabase.collection("JobAlert").get()
        for doc in docs:
            key = doc.id
            fdatabase.collection("JobAlert").document(key).delete()

        job_request = JobRequest()
        job_request.employee = employee
        job_request.job = job
        job_request.request_type = type
        job_request.save()

        # pusher_client.trigger(f'private-emp-{emp_id}-channel', 'job_request_trigger',
        # {
        #    'message': job_id
        # })

        data = {
            "job_id": job.id,
            "employee_id": employee.id,
            "job_client_name": job.client_name,
            "job_client_number": job.client_phone_number,
            "job_latlng": GeoPoint(job.lat, job.lng),
            "job_zone": job.zone,
            "job_remarks": job.remark,
            "job_address": job.address,
            "job_no": job.job_no,
            "Accept": "false",
            "created_at": fireview.SERVER_TIMESTAMP
        }
        fdatabase.collection("JobAlert").add(data)

        pusher_client.trigger(f'private-admin{request.user.username}-channel', 'job_request_feedback',
                              {
                                  'message': f"Job Sent to {emp_username} -- {type}",
                                  "type": 'success',
                                  "job_id": job.id,
                              })

        return HttpResponse(json.dumps({'status': "success"}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'status': "failed", 'error': logging.error(traceback.format_exc())}),
                            content_type="application/json")


####### LOGS ########
@user_passes_test(check_admin)
def view_job_request_logs(request):
    job_request = JobRequest.objects.all().order_by('-created_at')
    context = {
        "job_requests": job_request
    }
    return render(request, 'job_management/view_job_request_logs.html', context)


@user_passes_test(check_admin)
def view_job_assigned_logs(request):
    job_assign = JobAssign.objects.all().order_by('-created_at')
    context = {
        "job_assigns": job_assign
    }
    return render(request, 'job_management/view_job_assigned_logs.html', context)

