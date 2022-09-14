from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class User(AbstractUser):
    type = (
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor')
    )
    picture = models.ImageField(upload_to='photos/%Y/%m/%d')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField(validators=[MinValueValidator(100000),MaxValueValidator(999999)], null=True)
    Types_of_Users = models.CharField(choices=type, max_length=10, default=False)

    def __str__(self):
        return f"user : {self.username}   Type : {self.Types_of_Users}"


class PostsModel(models.Model):
    type = (
        ('1','Mental Health'),
        ('2','Heart Disease'),
        ('3','Covid19'),
        ('4','Immunization')
    )

    title = models.CharField(max_length=255)
    images = models.ImageField(upload_to='image/%Y/%m/%d')
    Category = models.CharField(choices=type, max_length=50)
    Content = models.TextField()
    username = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.title}   ->category: {self.Category}"


class AppointmentModel(models.Model):
    doctor_name = models.CharField(max_length=150)
    patient_name = models.CharField(max_length=150)
    speciality = models.CharField(max_length=150)
    date = models.DateField()
    start_Time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.speciality}  ---> docter : {self.doctor_name}"