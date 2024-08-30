
from django.urls import path
from core.panties import index
from . import views

app_name  = "core"

urlpatterns = [
    path("",views.index,name="index"),
    path("category/",views.category_list_view,name="category-list"),
    path("category/<cid>",views.product_list_category_view,name="category-product-list"),
    
    path("vendors/",views.vendor_list_view,name="vendor-list"),
    
    path("products/<pid>/",views.product_detail_view,name="product-detail"),
    
    path("products/tag/<slug:tag_slug>/", views.tag_list, name="tags"),
    
    path("ajax-add-review/<pid>/",views.ajax_add_review,name="ajax-add-review"),
    
    path("search/",views.search_view, name="search"),
    
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    
    path("cart/", views.cart_view, name="cart"),
    
]
