from django.db import models
from accounts.models import customer
from Shop_Product.models import Order

class courierList(models.Model):
    courierName = models.CharField(max_length=100)

    def __str__(self):
        return self.courierName

class courier(models.Model):
    CourierId = models.ForeignKey(courierList, on_delete=models.CASCADE)
    CustomerName = models.CharField(max_length=100)
    CustomerAddress = models.CharField(max_length=100)
    CustomerMobile = models.CharField(max_length=100)
    DeliveryStatus = models.CharField(max_length=100)
    OrderId = models.ForeignKey(Order, on_delete=models.CASCADE)


    def __str__(self):
        return self.CourierId
