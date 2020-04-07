from django.contrib import admin
from .models import customer, location, supplier
# Register your models here.

class locationAdmin(admin.ModelAdmin):
    list_display = ['State']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['CustomerId','CompanyName','PhoneNumber','Mobile','Country','Address','PostalCode','LocationId']

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['SupplierName','Mobile','Country','Address','LocationId','PostalCode']


admin.site.register(customer, CustomerAdmin)
admin.site.register(location, locationAdmin)
admin.site.register(supplier, SupplierAdmin)