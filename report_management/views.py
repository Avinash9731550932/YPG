from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from job_management.models import Job, JobReport, JobReportImage
from django.contrib.auth.models import User

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
# from reportlab.platypus import Image As Image1
from PIL import Image
import requests
from reportlab.lib.utils import ImageReader

from accounts.models import ETLog, EmployeeProfile
from .serializers import ETLogSerializer


# Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

import datetime


def check_admin(user):
   return user.is_superuser


@user_passes_test(check_admin)
def emp_travel_log(request, pk):
    employee = get_object_or_404(User, pk=pk)
    context ={
        'employee' :employee,
    }
    return render(request,"report_management/employee_route_activity.html", context)


@user_passes_test(check_admin)
def alarm_reponse_report(request, pk):

    job_report = get_object_or_404(JobReport, pk=pk)
     # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    
    c = canvas.Canvas(buffer, pagesize=A4)
    # imgDoc.setPageSize(A4) # This is actually the default page size

    document_width, document_height = A4
    document_width -= 20
    document_height -= 20
   
    c.setTitle(f'ALARM RESPONSE REPORT { job_report.id }')
    
    c.setStrokeColorRGB(0,0,0)
    c.setFont('Helvetica', 8)
    # draw some lines
 
    c.rect(x=0.35*inch,y=1.6*inch,width=7.6*inch, height=7.3*inch, fill=0)

    logo = ImageReader("https://securityappbucket.s3.amazonaws.com/media/images/company/ypg-security-logo.png")
    c.drawImage(logo, 0.35*inch, 10.8*inch, mask='auto')

    c.setFont('Helvetica-Bold', 11)
    c.drawString(0.35*inch, 10.4*inch, "Collins Street Tower")
    c.setFont('Helvetica-Bold', 11)
    c.drawString(0.35*inch, 10.2*inch, "Level 3, 480 Collins Street")
    c.setFont('Helvetica-Bold', 11)
    c.drawString(0.35*inch, 10*inch, "Melbourne VIC 3000")
    c.setFont('Helvetica', 11)
    c.drawString(0.35*inch, 9.7*inch, "admin@ypgrisk.com.au")
    c.setFont('Helvetica', 11)
    c.drawString(0.35*inch, 9.4*inch, "1300 690 099 ypgrisk.com.au")
    c.setFont('Helvetica', 11)
    c.drawString(0.35*inch, 9.1*inch, "SF #:6545-656-542")


    c.setFont('Helvetica-Bold', 15)
    c.drawString(7*inch, 10.4*inch, "ALARM")
    c.setFont('Helvetica-Bold', 15)
    c.drawString(6.6*inch, 10.15*inch, "RESPONSE")
    c.setFont('Helvetica-Bold', 15)
    c.drawString(6.9*inch, 9.9*inch, "REPORT")

    c.setFont('Helvetica-Bold', 15)
    c.setFillColorRGB(1,0,0)
    c.drawString(6.9*inch, 9.65*inch, str(job_report.id))

    # Draw hortizontal line client name
    # c.line(x1=0.35*inch,y1=8.9*inch,x2=7.95*inch,y2=8.9*inch)
    # c.drawString(0.5*inch, 8.55*inch, "CLIENT NAME: ")
    c.setFillColorRGB(0,0,0)
    y=8.55*inch
    x= 0.5*inch

    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, "CLIENT NAME:")
    textWidth = stringWidth("CLIENT NAME:", 'Helvetica-Bold',12) 
    x += textWidth + 0.2*inch
    c.setFont('Helvetica', 12)
    c.drawString(x, y, job_report.job.client_name)
    c.setFont('Helvetica', 8)
    
    

    # Draw hortizontal line client address
    c.line(x1=0.35*inch,y1=8.38*inch,x2=7.95*inch,y2=8.38*inch)

    x= 0.5*inch
    y= 8.1*inch

    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, "CLIENT ADDRESS:")
    # textWidth = stringWidth("CLIENT ADDRESS:", 'Helvetica-Bold',12) 
    # x += textWidth + 0.2*inch
    c.setFont('Helvetica', 12)

    job_address = job_report.job.address
    add_list1 =job_address[0:67]
    add_list2 =job_address[67:]
    c.drawString(2.2*inch, 8.1*inch, add_list1)
    c.drawString(0.5*inch, 7.58*inch, add_list2)


    # Draw hortizontal line client address2 decrease 0.52 => 8.38-0.52 = 7.86
    c.line(x1=0.35*inch,y1=7.86*inch,x2=7.95*inch,y2=7.86*inch)

    # Draw hortizontal line attendence notes
    c.line(x1=0.35*inch,y1=7.34*inch,x2=7.95*inch,y2=7.34*inch)

    x= 0.5*inch
    y= 7*inch
    
    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, "ATTENDANCE NOTES:")
    textWidth = stringWidth("ATTENDANCE NOTES:", 'Helvetica-Bold',12) 
    x += textWidth + 0.2*inch
    c.setFont('Helvetica', 12)
    c.drawString(x, y, job_report.attendance_note)
    c.setFont('Helvetica', 8)


    # Draw hortizontal line time on, off, job no
    c.line(x1=0.35*inch,y1=6.82*inch,x2=7.95*inch,y2=6.82*inch)

    x= 0.5*inch
    y= 6.5*inch
    
    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, "TIME ON:")
    textWidth = stringWidth("TIME ON:", 'Helvetica-Bold',12) 
    x += textWidth + 0.2*inch
    c.setFont('Helvetica', 12)
    c.drawString(x, y, job_report.time_on.strftime("%H:%M"))
    c.setFont('Helvetica', 8)


    c.setFont('Helvetica-Bold', 12)
    c.drawString(2.4*inch, y, "TIME OFF:")
    textWidth = stringWidth("TIME OFF:", 'Helvetica-Bold',12) 
    x += textWidth + 0.2*inch
    c.setFont('Helvetica', 12)
    c.drawString(3.4*inch, y, job_report.time_off.strftime("%H:%M"))
    c.setFont('Helvetica', 8)


    c.setFont('Helvetica-Bold', 12)
    c.drawString(4.7*inch, y, "JOB NO:")
    textWidth = stringWidth("JOB NO:", 'Helvetica-Bold',12) 
    x += textWidth + 0.2*inch
    c.setFont('Helvetica', 12)
    c.drawString(5.6*inch, y, job_report.job.job_no)
    c.setFont('Helvetica', 8)

    # Draw hortizontal line zone
    c.line(x1=0.35*inch,y1=6.30*inch,x2=7.95*inch,y2=6.30*inch)
    c.line(x1=2.15*inch,y1=6.30*inch,x2=2.15*inch,y2=6.83*inch)
    c.line(x1=4.15*inch,y1=6.30*inch,x2=4.15*inch,y2=6.83*inch)

    x= 0.5*inch
    y= 6*inch
    
    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, "ZONE:")
    textWidth = stringWidth("ZONE:", 'Helvetica-Bold',12) 
    x += textWidth + 0.2*inch
    c.setFont('Helvetica', 12)
    c.drawString(x, y, job_report.job.zone)
    c.setFont('Helvetica', 8)

    # Draw hortizontal bureu no
    c.line(x1=0.35*inch,y1=5.78*inch,x2=7.95*inch,y2=5.78*inch)
    x= 0.5*inch
    y= 5.48*inch
    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, "BUREU NO:")
    textWidth = stringWidth("BUREU NO:", 'Helvetica-Bold',12) 
    x += textWidth + 0.2*inch
    c.setFont('Helvetica', 12)
    if job_report.bureu != None:
        c.drawString(x, y, job_report.bureu)
    else:
        c.drawString(x, y, "")
    c.setFont('Helvetica', 8)


    # Draw hortizontal bureu no2
    c.line(x1=0.35*inch,y1=5.26*inch,x2=7.95*inch,y2=5.26*inch)

    # Draw hortizontal description
    c.line(x1=0.35*inch,y1=4.74*inch,x2=7.95*inch,y2=4.74*inch)

    x= 0.5*inch
    y= 4.44*inch
    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, "DESCRIPTION:")
    textWidth = stringWidth("DESCRIPTION:", 'Helvetica-Bold',12) 
    x += textWidth + 0.05*inch
    c.setFont('Helvetica', 12)
    # c.drawString(x, y, job_report.description)
    c.setFont('Helvetica', 12)

    description = job_report.description

    desc_list =[description[i:i+95] for i in range(0, len(description), 95)]

    desc_y = 3.9
    for desc in desc_list:
        c.drawString(0.5*inch, desc_y*inch, desc)
        desc_y -=0.52


    c.setFont('Helvetica', 12)

    c.line(x1=0.35*inch,y1=4.22*inch,x2=7.95*inch,y2=4.22*inch)
    c.line(x1=0.35*inch,y1=3.70*inch,x2=7.95*inch,y2=3.70*inch)
    c.line(x1=0.35*inch,y1=3.18*inch,x2=7.95*inch,y2=3.18*inch)
    c.line(x1=0.35*inch,y1=2.66*inch,x2=7.95*inch,y2=2.66*inch)
    c.line(x1=0.35*inch,y1=2.14*inch,x2=7.95*inch,y2=2.14*inch)

    c.line(x1=0.35*inch,y1=1.12*inch,x2=7.95*inch,y2=1.12*inch)

    c.drawString(0.45*inch, 1.29*inch, "ATTENDING OFFICER:")
    c.drawString(2.4*inch, 1.29*inch, job_report.employee.first_name +" "+ job_report.employee.last_name)
    c.setFont('Helvetica', 12)
    c.line(x1=0.35*inch,y1=0.62*inch,x2=7.95*inch,y2=0.62*inch)

    c.drawString(0.45*inch, 0.78*inch, "SIGNATURE:")
    c.setFont('Helvetica', 12)
    asiallogo = ImageReader("https://securityappbucket.s3.amazonaws.com/static/images/asial_logo.jpg")
    c.drawImage(asiallogo, 6.7*inch, 0.14*inch, 1.5*inch, 1.1*inch, mask='auto')

    # Add Page Number
    c.setFont('Helvetica', 8)
    c.drawString(10, 10, "1")

    c.showPage()


    job_report_images = JobReportImage.objects.filter(job_report = job_report)
    host_name =request.META['HTTP_HOST']
    counter = 2
    for job_report_image in job_report_images:
        img_path = f'http://{host_name}{job_report_image.image.url}'
        Image_file = Image.open(requests.get(img_path, stream=True).raw)
        # Open the image file to get image dimensions
        # Image_file = report_image
        image_width, image_height = Image_file.size
        image_aspect = image_height / float(image_width)

        # Determine the dimensions of the image in the overview
        print_width = document_width
        print_height = document_width * image_aspect

        if print_height > document_height:
            print_height = print_height/2
            print_width  = print_width/2


        # Draw the image on the current page
        # Note: As reportlab uses bottom left as (0,0) we need to determine the start position by subtracting the
        #       dimensions of the image from those of the document
        c.setFont('Helvetica', 8)
        c.drawString(10, document_height-5, f"JOB NO: {job_report.job.job_no}")

        c.drawImage(img_path, 10, document_height - (print_height+15), width=print_width, height=print_height)

        # Add Page Number
        c.setFont('Helvetica', 8)
        c.drawString(10, 10, str(counter))
        counter += 1

        c.showPage()
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    data = request.GET
    action = data.get('action', None)

    if action == "download":
        return FileResponse(buffer, as_attachment=True, filename=f'Alarm_response_{job_report.job.job_no}.pdf')
    else:
        return FileResponse(buffer, as_attachment=False, filename=f'Alarm_response_{job_report.job.job_no}.pdf')

class fetchEmpRouteActivity(APIView):
    def post(self, request, format=None):
        data = request.POST
        employee_id = data.get('employee_id', None)
        employee_date = data.get('employee_date', None)
        datef = datetime.datetime.strptime(employee_date, '%Y-%m-%d')

        nextday = datef + datetime.timedelta(1)
        datefstart = datetime.datetime.combine(datef, datetime.time())
        datefend = datetime.datetime.combine(nextday, datetime.time())
        print(datefstart)
        print(datefend)
        employee = get_object_or_404(User, pk=employee_id)
        etlogs = ETLog.objects.filter(employee_id = employee_id, created_at__lte=datefend, created_at__gte=datefstart).order_by('created_at')
        serializer = ETLogSerializer(etlogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@user_passes_test(check_admin)
def employeeTable(request):
    employees = EmployeeProfile.objects.all()

    context ={
        'employees' :employees
    }
    return render(request, 'report_management/employee_table.html', context)