from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    Gender = models.CharField(max_length=2, choices=[('M','Male'),('F','Female'),('T','Transgender')])
    DOB = models.DateField()
    number = models.IntegerField(unique=True)
    def __str__(self):
        return self.username
    
class Doctor(models.Model):
    Doctorname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    Gender = models.CharField(max_length=2, choices=[('M','Male'),('F','Female'),('T','Transgender')])
    DOB = models.DateField()
    number = models.IntegerField(unique=True)
    Medical_Degree = models.CharField(max_length=100)
    University_Name = models.CharField(max_length=100)
    Graduation_Year = models.IntegerField()
    Specialty = models.CharField(max_length=100)
    Address = models.TextField(max_length=500)
    Photo = models.ImageField(upload_to="profile_image/", blank=True, null=True)
    def __str__(self):
        return self.Doctorname