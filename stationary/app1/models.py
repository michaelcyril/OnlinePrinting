from unicodedata import name
from venv import create
from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    choice = (('owner', 'owner'), ('client', 'client'))
    type = models.CharField(max_length=100, choices=choice)
    phone = models.CharField(max_length=10)
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username    


class Stationery(models.Model):
    name = models.CharField(max_length=200 )
    logo= models.ImageField(upload_to="uploads/", null=True, blank=True)
    description = models.CharField(max_length=1000)
    location = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Document(models.Model):
    choice = (('pending', 'pending'), ('printed', 'printed'), ('taken', 'taken'))
    name = models.CharField(max_length=200)
    pages = models.IntegerField()
    file_doc = models.FileField(upload_to="pdfs/", null=True, blank=True)
    no_copies = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stationery_id = models.ForeignKey(Stationery, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=choice, default="pending")
    
class Cost(models.Model):
    stationery_id = models.ForeignKey(Stationery,on_delete=models.CASCADE)
    print_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    