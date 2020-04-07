from django.contrib import admin
from .models import Category, SubCategory, Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['CategoryName','CreatedBy','CreatedOn']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['SubCategoryName','CreatedBy','CreatedOn','CategoryId']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['CategoryId','SubCategoryId','ProductName','description','UnitPrice','Stock','created','updated','CreatedBy']
    list_editable = ['UnitPrice','Stock']

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product,ProductAdmin)