from django.shortcuts import render, redirect
from .forms import CategoryForm
from .models import Category, SubCategory, Product, Cart, Order, OrderDetail
from django.contrib import messages
from accounts.models import customer, location, supplier
from django.contrib.auth.models import User
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

    if not a:
        messages.success(request, "No Results Found")
    #subcategorys = SubCategory.objects.get(id=id)
    #subcategorys = SubCategory.objects.filter(CategoryId_id=id)
    return render(request,"showProducts.html",{'categorys':categorys, 'products':a, 'search_value': Product_search, 'count': counts})

def addToCart(request, uid, pid):
    flag = 0
    dfee = 0

    locationId = customer.objects.get(CustomerId_id=int(uid))
    print(locationId)
    clocation = locationId.LocationId_id
    print(clocation)

    cart_details = Cart.objects.filter(CustomerId_id=uid, ProductId_id=pid)
    if cart_details:
        cart_details = Cart.objects.get(CustomerId_id=uid, ProductId_id=pid)
        p = Product.objects.get(id=pid)
        if cart_details.Quantity < p.Stock:
            cart_details.Quantity += 1
            cart_details.Total = cart_details.Quantity * cart_details.Price
            cart_details.save()
        else:
            messages.info(request, 'Stock Limit Reached, Cannot Add More Quantity')
            flag = 1
    else:
        p = Product.objects.filter(id=pid)

        check = Product.objects.select_related('CreatedBy').get(id=pid)
        print(check.CreatedBy.LocationId_id)
        if check.CreatedBy.LocationId_id != clocation:
            dfee = dfee + 40

        for a in p:
            add_data = Cart(Price=a.UnitPrice, Quantity=1, CustomerId_id=uid, ProductId_id=pid, Total=a.UnitPrice, DeliveryCharges=dfee)
        add_data.save()

    categorys = Category.objects.all()
    products = Product.objects.all()[:12]

    if flag == 0:
        messages.success(request, 'Successfully Added To Cart!')

    return redirect('/show')
    #return render(request,"show.html",{'categorys':categorys, 'product_show': products, 'messages':'Added To Cart'})

def showUserCart(request, uid):
    items = Cart.objects.select_related('ProductId').filter(CustomerId_id=int(uid))
    #print(items.ProductName)
    sum = 0
    dfee = 0
    flag = 0
    for i in items:

        stock = i.ProductId.Stock
        quantity_product = i.Quantity
        if quantity_product <= stock:
            total = i.Price * i.Quantity
            sum = sum + total
            dfee = dfee + i.DeliveryCharges
        else:
            flag = 1

    if flag == 1:
        messages.info(request, "Please Remove Out of Stock Items to Place Order")
    elif sum == 0:
        messages.info(request, 'Your Cart Is Empty!')

    return render(request, "showUserCart.html",{'items':items, 'GrandTotal':sum+dfee, 'flag': flag})

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

def placeOrder(request, uid):
    items = Cart.objects.select_related('ProductId').filter(CustomerId_id=int(uid))
    quantity = 0
    total = 0
    dfee = 0
    flag = 0

    locationId = customer.objects.get(CustomerId_id=int(uid))
    print(locationId)
    clocation = locationId.LocationId_id
    print(clocation)
    if items:
        for i in items:
            stock = i.ProductId.Stock
            quantity_product = i.Quantity
            if quantity_product <= stock:
                quantity = quantity + i.Quantity
                total = total + i.Price*i.Quantity
                check = Product.objects.select_related('CreatedBy').get(id=i.ProductId_id)
                print(check.CreatedBy.LocationId_id)
                if check.CreatedBy.LocationId_id != clocation:
                    dfee = dfee + 40
            else:
                flag = 1
                messages.info("")
        if flag == 0:
            location_id = location.objects.get(id=clocation)
            user_id = User.objects.get(id=uid)

            order_data = Order(Quantity=quantity, LocationId=location_id, CustomerId=user_id, Total=total, DeliveryCharge=dfee)
            order_data.save()

            items = Cart.objects.select_related('ProductId').filter(CustomerId_id=int(uid))
            order = Order.objects.filter(CustomerId_id=uid).order_by('id')
            for o in order:
                order = o.id
                print(order)
                #break
            print('***********************************')

            order = Order.objects.get(id=order)
            for i in items:
                p = Product.objects.get(id=i.ProductId_id)
                print(p.id)
                p = Product.objects.get(id=p.id)
                total = i.Quantity*p.UnitPrice
                add_data = OrderDetail(OrderId=order, ProductId=p, Quantity=i.Quantity, Total=total)
                add_data.save()
                p.Stock = p.Stock - i.Quantity
                p.save()

            items = Cart.objects.select_related('ProductId').filter(CustomerId_id=int(uid))
            # print(items.ProductName)
            sum = 0
            for i in items:
                total = i.Price * i.Quantity
                sum = sum + total

            order = Order.objects.filter(CustomerId_id=uid).order_by('id')
            for o in order:
                order = o.id
                print(order)
                #break
            print('***********************************')

            order_detail = OrderDetail.objects.select_related('ProductId').filter(OrderId_id=order)

            Cart.objects.filter(CustomerId_id=uid).delete()

            messages.success(request, 'Order Placed Successfully!')

            dfee = Order.objects.filter(id=order)
            for d in dfee:
                dcharges = d.DeliveryCharge
            order_details = OrderDetail.objects.filter(OrderId_id=order).order_by('id')
            sum = 0
            for i in order_details:
                sum = sum + i.Total
            return render(request, "showOrder.html", {'items': order_details, 'GrandTotal':sum+dcharges, 'Dfee': dcharges})
            #return render(request, "showOrder.html", {'items': order_detail, 'GrandTotal': sum})
        else:
            return redirect('/showusercart/' + str(uid))

    else:
        return render(request, "showOrder.html")

def showOrder(request, uid):
    order = Order.objects.filter(CustomerId_id=uid).order_by('id')
    return render(request, "showOrder1.html", {'items': order})

def showOrderDetails(request, oid):
    dfee = Order.objects.filter(id=oid)
    for d in dfee:
        dcharges = d.DeliveryCharge
    order_details = OrderDetail.objects.filter(OrderId_id=oid).order_by('id')
    sum = 0
    for i in order_details:
        sum = sum + i.Total
    return render(request, "showOrderDetails.html", {'items': order_details, 'GrandTotal':sum+dcharges, 'Dfee': dcharges})

def supplierPage(request, uid):
    categorys = Category.objects.all()
    subcategory = SubCategory.objects.all()
    if request.method == 'POST':

        cid = request.POST['CategoryId']
        sid = request.POST['SubCategoryId']
        pname = request.POST['ProductName']
        pdesc = request.POST['Description']
        pimg = request.POST['imagepath']
        pup = request.POST['UnitPrice']
        pst = request.POST['Stock']
        supid = request.POST['user_id']

        pimg = "images/"+pimg

        add_data = Product(ProductName=pname, image=pimg, description=pdesc, UnitPrice=pup, Stock=pst, CategoryId_id=cid, CreatedBy_id=supid, SubCategoryId_id=sid)
        add_data.save()

        print("Added Successfully")

        return redirect('/showProductDetails/' + str(uid))
        #return redirect(request, "showInventory.html")
    else:
        return render(request, "showInventory.html", {'category': categorys, 'subcategory': subcategory, 'sid': uid})

def updateProductDetails(request, uid, pid):


    #product = Product.objects.get(id=pid)
    product = Product.objects.select_related('CategoryId', 'SubCategoryId').get(id=pid)
    #subcategory = SubCategory.objects.all()
    if request.method == 'POST':
        pup = request.POST['UnitPrice']
        pst = request.POST['Stock']
        product.Stock = pst
        product.UnitPrice = pup
        product.save()
        return redirect('/showProductDetails/' + str(uid))
    else:
        return render(request, "showInventoryUpdate.html", {'sid': uid, 'product': product, 'pid': pid})
    #return redirect('/showProductDetails/' + str(uid))

def showProductDetails(request, uid):

    product = Product.objects.filter(CreatedBy_id=uid)

    return render(request, "showProductDetails.html", {'items': product, 'sid': uid})

def deleteProductDetails(request, uid, pid):

    Product.objects.filter(pk=pid).delete()

    return redirect('/showProductDetails/' + str(uid))