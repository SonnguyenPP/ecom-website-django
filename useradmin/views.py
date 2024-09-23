from django.shortcuts import render, redirect
from core.models import CartOrder , Product, Category  , CartOrderItems,ProductReview
from django.db.models import Sum
from userauths.models import User
from django.db.models.functions import ExtractMonth
from django.views.decorators.csrf import csrf_exempt
import datetime
from useradmin.forms import AddProductForm
from django.contrib import messages

def dashboard(request):
    revenue = CartOrder.objects.aggregate(price = Sum("price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")
    latest_orders = CartOrder.objects.all()
    this_month = datetime.datetime.now().month
    monthly_revenue = CartOrder.objects.annotate(
    order_date_month=ExtractMonth('order_date')
).filter(order_date_month=this_month).aggregate(price=Sum('price'))
    
    context = {
        
        "revenue":revenue,
        "total_orders_count":total_orders_count,
        "all_products":all_products,
        "all_categories":all_categories,
        "new_customers":new_customers,
        "latest_orders":latest_orders,
        "monthly_revenue":monthly_revenue,
        
    }
    return render(request, "useradmin/dashboard.html",context)
    
    
def products(request):
    all_products = Product.objects.all().order_by("-id")
    all_categories = Category.objects.all()
    
    context = {
        
        "all_products":all_products,
        "all_categories":all_categories,   
    }
    return render(request, "useradmin/products.html",context)
    

    
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:dashboard")
    else:
        form = AddProductForm()
        
    context = {
        "form":form
        
    }   
    return render(request,"useradmin/add-product.html"
                  ,context)
    
def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:edit_product",product.pid)
    else:
        form = AddProductForm(instance=product)
        
    context = {
        "form":form,
        "product":product,
        
    }   
    return render(request,"useradmin/edit-product.html",context)



def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("useradmin:products")

def orders(request):
    orders = CartOrder.objects.all()
    context = {
        "orders":orders,
    }
    return render(request,"useradmin/orders.html",context)


def order_detail(request,id):
    order = CartOrder.objects.get(id=id) 
    order_items = CartOrderItems.objects.filter(order = order)
    context = {
        "order":order,
        "order_items":order_items,
        
    }
    return render(request,"useradmin/order_detail.html",context)


@csrf_exempt
def change_order_status(request,oid):
    order = CartOrder.objects.get(oid= oid)
    if request.method == 'POST':
        status = request.POST.get("status")
        print("status =====",status)
        order.product_status = status
        order.save()
        messages.success(request,f"Order status changed to {status}")
        
    return redirect('useradmin:order_detail',order.id)


def shop_page(request):
    products = Product.objects.all()
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_sales = CartOrderItems.objects.filter(order__paid_status = True).aggregate(qty=Sum("qty"))
    
    context = {
        "products":products,
        "revenue":revenue,
        "total_sales":total_sales,
        
    }
    return render(request,"useradmin/shop_page.html",context)
    
    
def reviews(request):
    reviews = ProductReview.objects.all()
    
    context = {
        "reviews":reviews
    }
    return render(request,"useradmin/reviews.html",context)
        
        
        
        
     