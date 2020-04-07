"""ShopOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from Shop_Product import views

urlpatterns = [
    path('', include('ecommerce.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    #path('shop/', include('shop.urls', namespace='shop')),
    path('cat', views.cat),
    path('show', views.show),
    path('edit/<int:id>', views.showSubCategory),
    path('edit/<int:id>/<int:sid>', views.showProduct),
    path('search', views.SearchProduct),
    path('addtocart/<int:uid>/<int:pid>', views.addToCart),
    path('showusercart/<int:uid>', views.showUserCart),
    path('showOrder/<int:uid>', views.showOrder),
    path('showOrderDetails/<int:oid>', views.showOrderDetails),
    path('addquantity/<int:uid>/<int:cid>', views.addQuantity),
    path('subquantity/<int:uid>/<int:cid>', views.subQuantity),
    path('deleteitem/<int:uid>/<int:cid>', views.deleteItem),
    path('placeOrder/<int:uid>/', views.placeOrder),
    path('update/<int:id>', views.update),
    path('delete/<int:id>', views.destroy),
    path('supplierPage/<int:uid>', views.supplierPage),
    path('showProductDetails/<int:uid>', views.showProductDetails),
    path('updateProduct/<int:uid>/<int:pid>', views.updateProductDetails),
    path('deleteProduct/<int:uid>/<int:pid>', views.deleteProductDetails),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)