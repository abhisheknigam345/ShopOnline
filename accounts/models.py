from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class location(models.Model):
    State = models.CharField(max_length=30)

    def __str__(self):
        return self.State

class customer(models.Model):
    CustomerId = models.OneToOneField(User, on_delete=models.CASCADE)
    CompanyName = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=100)
    Mobile = models.CharField(max_length=100)
    Country = models.CharField(max_length=50)
    Address = models.CharField(max_length=120)
    PostalCode = models.PositiveIntegerField()
    LocationId = models.ForeignKey(location, on_delete=models.CASCADE)

    #def __str__(self):
    #    return self.CustomerId

class supplier(models.Model):
    SupplierUserName = models.CharField(max_length=20)
    Password = models.CharField(max_length=30)
    SupplierName = models.CharField(max_length=100)
    Email = models.CharField(max_length=50)
    Mobile = models.CharField(max_length=100)
    Country = models.CharField(max_length=50)
    Address = models.CharField(max_length=120)
    LocationId = models.ForeignKey(location, on_delete=models.CASCADE)
    PostalCode = models.PositiveIntegerField()

    def __str__(self):
        return self.SupplierName
