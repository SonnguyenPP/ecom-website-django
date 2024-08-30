from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_list_or_404
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from django.db.models import Count, Avg
from taggit.models import Tag
from core.form import ProductReviewForm


def index(requets):
    
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured = True)
    
    context = {
        'products':products
    }
    return render(requets,'core/index.html',context)

def category_list_view(request):
    
    categories = Category.objects.all()
    
    context = {
        "categories" : categories
    }
    return render(request,'core/categories.html', context)

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

def product_detail_view(request,pid):
    
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(category = product.category).exclude(pid=pid)
    reviews = ProductReview.objects.filter(product=product)
    
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    review_form = ProductReviewForm()
    
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
    
    average_reviews = ProductReview.objects.filter(product = product).aaggregate(rating=Avg("rating"))
    return JsonResponse(
        {
        'bool': True,
        'context':context,
        'average_reviews':average_reviews 
        }
    )
    
    
def search_view(request):
    
    query = request.GET.get("q")
        
    products = Product.objects.filter(title__icontains=query, description__icontains = query).order_by("-date")
        
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
         'price': request.GET['price']
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            
            
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id,item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        
        return render(request, "core/cart.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})