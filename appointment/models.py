from django.db import models

# Create your models here.

class User(models.Model):
    uid = models.CharField(max_length=50, primary_key=True)
    upassword = models.CharField(max_length=100)
    uname = models.CharField(max_length=100)
    uphone = models.CharField(max_length=20)
    uemail = models.EmailField(unique=True)

class Owner(models.Model):
    owid = models.CharField(max_length=50, primary_key=True)
    opassword = models.CharField(max_length=100)
    owname = models.CharField(max_length=100)
    owphone = models.CharField(max_length=20)
    owapprove = models.BooleanField(default=False)

class Printer(models.Model):
    pid = models.AutoField( primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    pname = models.CharField(max_length=100)
    pdescription = models.TextField()

class Appointment(models.Model):
    appointmentId = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Printer, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    programme = models.CharField(max_length=100)
    appointmentStatus = models.CharField(max_length=20, default='Pending')
