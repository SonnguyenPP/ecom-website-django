from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_list_or_404
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address, Coupon

from taggit.models import Tag
from django.template.loader import render_to_string
from core.form import ProductReviewForm
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.core import serializers

import calendar
from django.db.models import Count, Avg
from django.db.models.functions import ExtractMonth

from userauths.models import ContactUs

from userauths.models import Profile

import stripe

from django.conf import settings

def index(requets):
    
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured = True)
    
    context = {
        'products':products
    }
    return render(requets,'core/index.html',context)

def category_list_view(request):
    
    categories = Category.objects.all()
    # .annotate(product_count = Count("product"))
    
    context = {
        "categories" : categories
    }
    return render(request,'core/categories.html', context)

# def category_product_list_view(request, cid):
#     category = Category.object.get(cid = cid)
#     products = Product.objects.filter(product_status="published",category = category)
    
#     context ={
#         "category": category,
#         "products": products,
#     }
#     return render(request, "core/category-product-list.html", context)

def product_list_view(request):
    
    products = Product.objects.filter(product_status= "published")
    
    context = {
        "products":products
    }
    
    return render(request,'core/product-list.html',context)

def product_list_category_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category= category)
    
    context = {
        "category":category,
        "products":products,
    }
    return render(request,"core/category-productlist.html",context)

def vendor_list_view(request):
    vendor = Vendor.objects.all()
    context = {
        "vendor" : vendor,
    }
    return render(request, "core/vendor-list.html",context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid = vid)
    products = Product.objects.filter( vendor= vendor, product_status="published")
    context = {
        "vendor" : vendor,
        "products":products,
    }
    return render(request, "core/vendor-detail-list.html",context)
    
    
    

def product_detail_view(request,pid):
    
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(category = product.category).exclude(pid=pid)
    reviews = ProductReview.objects.filter(product=product)
    
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    review_form = ProductReviewForm()
    
    make_review = True
    
    if request.user.is_authenticated:
        
        user_review_count = ProductReview.objects.filter(user = request.user, product = product).count()
        
        if user_review_count > 0:
            make_review = False
    
    
    context = {
        "product":product,
        "review_form":review_form,
        "p_image":p_image,
        "products":products,
        "reviews":reviews,
        "average_rating":average_rating,
    }
    
    return render(request,"core/product-detail.html",context)

def tag_list(request, tag_slug = None):
    
    product = Product.objects.filter(product_status = "published").order_by("id")
    
    tag = None
    
    if tag_slug:
        tag = get_list_or_404(Tag, slug = tag_slug)
        products = product.filter(tags__in=[tag])
        
    context ={
        "products" : products
    }
    
    return render(request,"core/tag.html",context)




def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating']
    )
    context = {
        'user' : user.username,
        'review': request.POST['review'],
        'rating':request.POST['rating'],
    }
    
    average_reviews = ProductReview.objects.filter(product = product).aggregate(rating=Avg("rating"))
    
    return JsonResponse(
        {
        'bool': True,
        'context':context,
        'average_reviews':average_reviews 
        }
    )
    
    
def search_view(request):
    
    query = request.GET.get("q")
        
    products = Product.objects.filter(title__icontains=query).order_by("-date")
        
    context = {
            "products":products,
            "query":query,
        }
    return render(request, "core/search.html", context)

def add_to_cart(request):
    
    cart_product = {}
    
    cart_product[str(request.GET['id'])] = {
         'title':request.GET['title'],
         'qty': request.GET['qty'],
         'price': request.GET['price'],
         'image':request.GET['image'],
         'pid':request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            
            
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
            
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj'])})

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    
    min_price   = request.GET['min_price']
    max_price   = request.GET['max_price']
    
    products = products.filter(price__gte = min_price)
    products = products.filter(price__lte = max_price)
    
    
    
    if len(categories) > 0 :
        products = products.filter(category__id__in = categories).distinct()
    if len(vendors) > 0 :
        products = products.filter(vendor__id__in = vendors).distinct()
        
    data = render_to_string("core/asyns/product-list.html",{"products":products})
    
    return JsonResponse({"data":data})


def cart_view(request): 
    cart_total_amount = 0
    
    # return render(request,"core/cart.html")
    
    if 'cart_data_obj' in request.session:
        for p_id,item in request.session['cart_data_obj'].items():
            
            cart_total_amount += int(item['qty']) * float(item['price'])
            
        return render(request, "core/cart.html",
                      {"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    
    else:
        messages.warning(request,"your cart is empty")
        return render(request, "core/cart.html")
    
    
    
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
         cart_data = request.session['cart_data_obj']
         del request.session['cart_data_obj'][product_id]
         request.session['cart_data_obj']= cart_data
        
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id,item in request.session['cart_data_obj'].items():
            
            cart_total_amount += int(item['qty']) * float(item['price'])
    context = render_to_string("core/asyns/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
            
        
        
    return JsonResponse({"data":context,'totalcartitems':len(request.session['cart_data_obj'])})

def update_from_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
         cart_data = request.session['cart_data_obj']
         cart_data[str(request.GET['id'])]['qty']= product_qty
         request.session['cart_data_obj']= cart_data
        
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id,item in request.session['cart_data_obj'].items():
            
            cart_total_amount += int(item['qty']) * float(item['price'])
    context = render_to_string("core/asyns/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
            
        
        
    return JsonResponse({"data":context,'totalcartitems':len(request.session['cart_data_obj'])})


def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        request.session["full_name"] = full_name
        request.session["email"] = email
        request.session["mobile"] = mobile
        request.session["address"] = address
        request.session["city"] = city
        request.session["state"] = state
        request.session["country"] = country
         
        if 'cart_data_obj' in request.session:
        
          for p_id,item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty'])* float(item['price'])
           
          order = CartOrder.objects.create(
            
            user = request.user,
            price = total_amount,
            full_name = full_name,
            email = email,
            phone = mobile,
            address = address,
            city = city,
            state = state,
            country =country,
            
         ) 
         
          del request.session["full_name"] 
          del request.session["email"] 
          del request.session["mobile"] 
          del request.session["address"] 
          del request.session["city"] 
          del request.session["state"] 
          del request.session["country"] 
         
          for p_id,item in request.session['cart_data_obj'].items():
           cart_total_amount += int(item['qty'])* float(item['price'])
           
           cart_order_products = CartOrderItems.objects.create(
               
               order = order,
               invoice_no = "INVOICE_NO-" + str(order.id),
               item = item['title'],
               image = item['image'],
               qty = item['qty'],
               price = item['price'],
               total = float(item['qty'])*float(item['price']),
               
               
           )
     
     
        return redirect("core:checkout",order.oid) 
    return redirect("core:checkout",order.oid) 
    
 
        
        
        

def checkout(request,oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)
   
    
    if request.method == "POST":
        code = request.POST.get("code")
        
        coupon = Coupon.objects.filter(code = code, active = True).first()
        if coupon:
            if coupon in order.coupons.all():
                messages.warning(request, "Coupon already")
                return redirect("core:checkout",order.oid)
            else:
                
                discount = order.price * coupon.discount / 100
                order.coupons.add(coupon)
                order.price -= discount
                order.saved += discount
                order.save()
                
                
                messages.success(request, "Coupon ativated")
                return redirect("core:checkout",order.oid)
        else:
            messages.warning(request, "Coupon do not exist")
            return redirect("core:checkout",order.oid)
    
    context ={
        "order":order,
        "order_items":order_items,
        "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,
    } 
    
    return render(request,"core/checkout.html",context)








@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0
    
    if 'cart_data_obj' in request.session:
        
        for p_id,item in request.session['cart_data_obj'].items():
           total_amount += int(item['qty'])* float(item['price'])
           
        order = CartOrder.objects.create(
            
            user = request.user,
            price = total_amount
            
        ) 
        for p_id,item in request.session['cart_data_obj'].items():
           cart_total_amount += int(item['qty'])* float(item['price'])
           
           cart_order_products = CartOrderItems.objects.create(
               
               order = order,
               invoice_no = "INVOICE_NO-" + str(order.id),
               item = item['title'],
               image = item['image'],
               
               qty = item['qty'],
               
               price = item['price'],
               total = float(item['qty'])*float(item['price']),
               
               
           )
           host = request.get_host()
           paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount':cart_total_amount ,
                'item_name':"Order-Item-No-" + str(order.id),
                'invoice':"INVOICE_NO-"+ str(order.id),
                'currency_code':"USD",
                'notify_url':'http://{}{}'.format(host,reverse("core:paypal-ipn")),
                'return_url':'http://{}{}'.format(host,reverse("core:payment-competed")),
                'cancel_return':'http://{}{}'.format(host,reverse("core:payment-failed")),
            }
    
           paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    # cart_total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for p_id,item in request.session['cart_data_obj'].items():
            
    #         cart_total_amount += int(item['qty']) * float(item['price'])
           try:
              active_address = Address.objects.get(user=request.user,status=True)
       
           except:
              messages.warning(request,"these are mutiplr address")
              active_address = None
    
           return render(request, "core/checkout.html",
                      {"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount,'active_address':active_address, 'paypal_payment_button':paypal_payment_button})
        
@csrf_exempt 
def create_checkout_session(request,oid):
    order = CartOrder.objects.get(oid=oid)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    checkout_session = stripe.checkout.Session.create(
        customer_email= order.email,
        payment_method_types= ['card'],
        line_items=[{
            'price_data':{
                'currency':"USD",
                'product_data':{
                    'name':order.full_name,
                },
                'unit_amount': int(order.price * 1000)
            },
            'quantity':1
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse("core:payment-completed",args=[order.id])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("core:payment-failed"))
        
    )
    order.paid_status = False
    order.stripe_payment_intent = checkout_session['id']
    order.save()
    
    return JsonResponse({"sessionId": checkout_session.id})
    
    

@login_required
def payment_completed_view(request,oid):
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'core/payment-completed.html',  {"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount} )


@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')


@login_required
def customer_dashboard(request):
    
    
    orders_list = CartOrder.objects.filter(user = request.user).order_by("-id")
    address = Address.objects.filter(user = request.user)
    
    orders = CartOrder.objects.annotate(month= ExtractMonth("order_date")).values("month").annotate(count = Count("id")).values("month","count")
    month = []
    total_orders = []
    
    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i["count"])
    
    
    if request.method == "POST":
      address = request.POST.get("address")
      mobile = request.POST.get("mobile")
    
      new_address = Address.objects.create(
           user=request.user,
           title=address,
           mobile=mobile
       )
      messages.success(request, "Address Added Successfully.")
      return redirect("core:dashboard")

    user_profile  = Profile.objects.get(user = request.user)
    print("user profile",user_profile)
    
    context = {
        "user_profile":user_profile,
        "orders":orders,
        "orders_list": orders_list,
        "address": address,
        "month": month,
        "total_orders": total_orders,
        
        
    }
    return render(request,'core/dashboard.html',context)


def order_detail(request, id):
    order = CartOrder.objects.get(user = request.user, id =id)
    order_items = CartOrderItems.objects.filter(order = order)
    
    context = {
        "order_items":order_items
    }
    return render(request,'core/order-detail.html', context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        "wishlist": wishlist
    }
    return render(request, "core/wishlist.html", context)


def add_to_wishlist(request):
    
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    
    context = {}
    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)
    
    
    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        context = {
            "bool": True
        }
    return JsonResponse(context)

def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)

    product = Wishlist.objects.get(id=id)
    product.delete()

    context = {
        "bool": True,
        "wishlist": wishlist
    }
    wishlist_json = serializers.serialize('json',wishlist)

    t = render_to_string("core/async/wishlist-list.html",context)
    return JsonResponse({"data":t, "w":wishlist_json})


def contact(request):
    return render(request,"core/contact.html")

def ajax_contact_form(request):
    email = request.GET['email']
    full_name = request.GET['full_name']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        email=email,
        full_name=full_name,
        phone=phone,
        subject=subject,
        message=message
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }

    return JsonResponse({"data": data})



