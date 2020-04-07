from django.shortcuts import render, redirect
from .forms import CategoryForm
from .models import Category, SubCategory, Product, Cart
from django.contrib import messages
import mysql.connector



def cat(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = CategoryForm()
    return render(request,'category.html',{'form':form})

def show(request):
    categorys = Category.objects.all()

    products = Product.objects.all()[:12]

    return render(request,"show.html",{'categorys':categorys, 'product_show': products})

def edit(request, id):
    category = Category.objects.get(id=id)
    return render(request,'edit.html', {'categorys':category})

def update(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(request.POST, instance = category)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, 'edit.html', {'categorys': category})

def destroy(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect("/show")

def show(request):
    categorys = Category.objects.all()
    products = Product.objects.all()[:12]
    return render(request,"show.html",{'categorys':categorys, 'product_show': products})

def showSubCategory(request, id):

    if id == 0:
        categorys = Category.objects.all()
        products = Product.objects.all()
        return render(request,"show.html",{'categorys':categorys, 'product_show': products})
    else:
        categorys = Category.objects.all()
        # subcategorys = SubCategory.objects.get(id=id)
        subcategorys = SubCategory.objects.filter(CategoryId_id=id)
        products = Product.objects.filter(CategoryId_id=id)
        return render(request, "show.html",{'categorys': categorys, 'subcategorys': subcategorys, 'product_show': products})

def showProduct(request, id, sid):
    categorys = Category.objects.all()
    #subcategorys = SubCategory.objects.get(id=id)
    subcategorys = SubCategory.objects.filter(CategoryId_id=id)
    products = Product.objects.filter(SubCategoryId_id=sid)
    return render(request,"show.html",{'categorys':categorys, 'subcategorys':subcategorys, 'products':products})

def SearchProduct(request):

    count = 0
    counts = []
    if request.method == 'POST':
        Product_search = request.POST['search_product']
        Category_id = request.POST['search_category']
        if Category_id == '0':
            print("*********1******")
            a = Product.objects.filter(ProductName__icontains=Product_search)
        else:
            print("*********2******")
            a = Product.objects.filter(ProductName__icontains=Product_search, CategoryId_id=Category_id)

    for i in a:
        count = count+1
        counts.append(count)
    print(count)

    categorys = Category.objects.all()
    #subcategorys = SubCategory.objects.get(id=id)
    #subcategorys = SubCategory.objects.filter(CategoryId_id=id)
    return render(request,"showProducts.html",{'categorys':categorys, 'products':a, 'search_value': Product_search, 'count': counts})

def addToCart(request, uid, pid):
    flag = 0
    cart_details = Cart.objects.filter(CustomerId_id=uid, ProductId_id=pid)
    if cart_details:
        cart_details = Cart.objects.get(CustomerId_id=uid, ProductId_id=pid)
        cart_details.Quantity += 1
        cart_details.Total = cart_details.Quantity * cart_details.Price
        cart_details.save()
    else:
        p = Product.objects.filter(id=pid)
        for a in p:
            add_data = Cart(Price=a.UnitPrice, Quantity=1, CustomerId_id=uid, ProductId_id=pid, Total=a.UnitPrice)
        add_data.save()

    categorys = Category.objects.all()
    products = Product.objects.all()[:12]

    messages.success(request, 'Successfully Added To Cart!')
    return redirect('/show')
    #return render(request,"show.html",{'categorys':categorys, 'product_show': products, 'messages':'Added To Cart'})

def showUserCart(request, uid):
    items = Cart.objects.select_related('ProductId').filter(CustomerId_id=int(uid))
    #print(items.ProductName)
    sum = 0
    for i in items:
        total = i.Price*i.Quantity
        sum = sum + total

    return render(request, "showUserCart.html",{'items':items, 'GrandTotal':sum})

def addQuantity(request, uid, cid):
    items = Cart.objects.get(pk=cid)
    items.Quantity = items.Quantity + 1
    items.Total = items.Quantity * items.Price
    items.save()
    #return render(request, "showUserCart.html")
    return redirect('/showusercart/'+str(uid))

def subQuantity(request, uid, cid):
    items = Cart.objects.get(pk=cid)
    if items.Quantity != 1:
        items.Quantity = items.Quantity - 1
        items.Total = items.Quantity * items.Price
        items.save()
        return redirect('/showusercart/'+str(uid))
    else:
        return redirect('/deleteitem/'+str(uid)+'/'+str(cid))

def deleteItem(request, uid, cid):
    Cart.objects.filter(pk=cid).delete()
    return redirect('/showusercart/'+str(uid))