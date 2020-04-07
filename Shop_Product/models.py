from django.db import models
from accounts.models import supplier, location
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    CategoryId = models.IntegerField
    CategoryName = models.CharField(max_length=30)
    CreatedBy = models.CharField(max_length=30)
    CreatedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.CategoryName

class SubCategory(models.Model):
    SubCategoryId = models.IntegerField
    SubCategoryName = models.CharField(max_length=30, db_index=True)
    CreatedBy = models.CharField(max_length=30, db_index=True)
    CreatedOn = models.DateTimeField(auto_now_add=True)
    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.SubCategoryName

class Product(models.Model):
    ProductId = models.IntegerField
    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    SubCategoryId = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    ProductName = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', blank=True)
    description = models.TextField(blank=True)
    UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    Stock = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    CreatedBy = models.ForeignKey(supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.ProductName

class Cart(models.Model):
    CartId = models.IntegerField
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Quantity = models.PositiveIntegerField()
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    CustomerId = models.ForeignKey(User, on_delete=models.CASCADE)
    Total = models.DecimalField(max_digits=10, decimal_places=2)
    DeliveryCharges = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    OrderId = models.IntegerField
    OrderDate = models.DateTimeField(auto_now=True)
    Quantity = models.PositiveIntegerField()
    LocationId = models.ForeignKey(location, on_delete=models.CASCADE)
    CustomerId = models.ForeignKey(User, on_delete=models.CASCADE)
    Total = models.DecimalField(max_digits=10, decimal_places=2)
    DeliveryCharge = models.DecimalField(max_digits=5, decimal_places=2)
    DeliveryStatus = models.CharField(max_length=15, default='Pending')

class OrderDetail(models.Model):
    OrderDetailId = models.IntegerField
    OrderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.PositiveIntegerField()
    Total = models.DecimalField(max_digits=10, decimal_places=2)
