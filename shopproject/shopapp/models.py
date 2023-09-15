from django.db import models

# Create your models here.
class merchant(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    phone = models.IntegerField()
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    phone = models.IntegerField()
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class merchant_service_details(models.Model):
    company_name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, default="health")
    title = models.CharField(max_length=100)
    description = models.TextField()
    charges = models.DecimalField(max_digits=6, decimal_places=2)
    start_time = models.TimeField(auto_now=False, default='20:00')
    end_time = models.TimeField(auto_now=False, default='20:00')
    image = models.ImageField(upload_to='images/')  # Specify the upload directory here
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)