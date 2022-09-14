from django.shortcuts import redirect, render
from .models import User, PostsModel,AppointmentModel
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def dashboard(request):

    current_user = request.user
    item = User.objects.get(id=current_user.id)
    return render(request, 'home/dashboard.html', {'item':item})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    return render(request, 'home/login.html')


def sinup(request):
    if request.method == "POST":
        # print("hello")
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        picture = request.FILES['picture']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        Types_of_Users = request.POST['Types_of_Users']

        if len(password)<8:
            messages.error(request, "Password Not Secure")
            return redirect('sinup')
        else:
            if password==confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists!")
                    return redirect('sinup')
                else:
                    if  User.objects.filter(email=email).exists():
                        messages.error(request, "Email already exists!")
                        return redirect('sinup')
                    else:
                        user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password, picture=picture, address=address, city=city, state=state, pincode=pincode, Types_of_Users=Types_of_Users)
                        user.save()
                        messages.success(request, 'You are registered successfully. you are login')
                        return redirect('login')
            else:
                messages.error(request, "Password do not match.")
                return redirect('sinup')
    else:
        # types = User.objects.values_list('Types_of_Users', flat=True).distinct()
        return render(request, 'home/sinup.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request,'You are successfully logged out.')
        return redirect('login')
    return redirect('home')


@login_required(login_url='login')
def post(request):
    # pass
    if request.method == "POST":
        title = request.POST['title']
        images = request.FILES['images']
        Category = request.POST['Category']
        Content = request.POST['Content']
        user = request.user
        UserName = user.username
        a = title.split(' ')
        slug = '-'.join(a)
        blog = PostsModel(title=title, images=images, Category=Category, Content=Content, username=UserName, slug=slug)
        blog.save()
        messages.success(request, 'Blog post successfully created.')
        return redirect('post')

    return render(request, 'home/post.html')


@login_required(login_url='login')
def all(request):
    user = request.user
    if user.Types_of_Users == 'Doctor':
        object = PostsModel.objects.filter(username=user.username)
        item1 = object.filter(Category='1')
        item2 = object.filter(Category='2')
        item3 = object.filter(Category='3')
        item4 = object.filter(Category='4')
    else:
        item1 = PostsModel.objects.filter(Category='1')
        item2 = PostsModel.objects.filter(Category='2')
        item3 = PostsModel.objects.filter(Category='3')
        item4 = PostsModel.objects.filter(Category='4')
    data = {
        'item1':item1,
        'item2':item2,
        'item3':item3,
        'item4':item4,
    }
    return render(request, 'home/all.html', data)


@login_required(login_url='login')
def detail(request, slug):
    item = PostsModel.objects.get(slug=slug)
    data = {
        'item':item
    }
    return render(request, 'home/detail.html', data)


@login_required(login_url='login')
def all_doctor(request):
    item = User.objects.filter(Types_of_Users='Doctor')
    data = {
        'items':item
    }
    return render(request, 'home/all_doctor.html', data)



def PatientAppointment(request):
    i = request.user.username
    item = AppointmentModel.objects.filter(patient_name=i)

    return render(request, 'home/PatientAppointment.html',{'items':item})

def showAppointment(request):
    i = request.user.username
    item = AppointmentModel.objects.filter(doctor_name=i)
    return render(request, 'home/showAppointment.html',{'items':item})




import os
from decouple import config
from google.oauth2 import service_account
from googleapiclient.discovery import build
# import datetime


# Google service account
SCOPES = ["https://www.googleapis.com/auth/calendar"]

service_account_email = config('service_account_email')

credentials = service_account.Credentials.from_service_account_file('./banao-django.json')
scoped_credentials = credentials.with_scopes(SCOPES)
calendarId = config('calendarId')

def build_service(request):

    service = build("calendar", "v3", credentials=scoped_credentials)
    return service


from datetime import datetime,time, timedelta
def appointment(request,id):
    if request.method == 'POST':
        i = User.objects.get(id=id)
        doctor_name =  i.username
        speciality = request.POST['speciality']
        date = request.POST['date']
        start_Time = request.POST['appointment_time']
        patient_name = request.user.username
        print(start_Time, type(start_Time))
        print(date,speciality,doctor_name,patient_name)

        d1 = date+' '+start_Time
        startTime = datetime.strptime(d1, '%Y-%m-%d %H:%M')
        print(startTime)

        s = datetime.strptime(start_Time, '%H:%M')

        end = s + timedelta(minutes=45)
        c = str(end)
        d2 = date+c[10:]

        endTime = datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
        print(endTime)

        service = build_service(request)

        event = (
            service.events().insert(
                calendarId=calendarId,
                body={
                    "summary": speciality,
                    "start": {"dateTime": startTime.isoformat(), 'timeZone': 'Asia/Kolkata',},
                    "end": {"dateTime": endTime.isoformat(), 'timeZone': 'Asia/Kolkata',},
                },
            ).execute()
        )

        print(event)


        data = AppointmentModel(doctor_name=doctor_name, patient_name=patient_name, speciality=speciality, date=date, start_Time=start_Time, end_time=end)
        data.save()
        messages.success(request, 'successfully Appointment.')
        return redirect('PatientAppointment')

    return render(request, 'home/appointment.html', {'item':id})
