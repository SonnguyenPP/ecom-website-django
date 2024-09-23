
from django.urls import path, include
from core.panties import index
from . import views

app_name  = "core"

urlpatterns = [
    path("",views.index,name="index"),
    
    path("products/",views.product_list_view,name="product-list"),
    
    path("category/",views.category_list_view,name="category-list"),
    path("category/<cid>",views.product_list_category_view,name="category-product-list"),
    
    path("vendors/",views.vendor_list_view,name="vendor-list"),
    path("vendors/<vid>",views.vendor_detail_view,name="vendor-detail"),
    
    
    path("products/<pid>/",views.product_detail_view,name="product-detail"),
    path("products/tag/<slug:tag_slug>/", views.tag_list, name="tags"),
    
    
    path("ajax-add-review/<int:pid>/",views.ajax_add_review,name="ajax-add-review"),
    
    path("search/",views.search_view, name="search"),
    
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    
    path("cart/", views.cart_view, name="cart"),
    
    path("filter-products/", views.filter_product, name="filter-product"),
    
    path("delete-from-cart/", views.delete_item_from_cart,name="delete-from-cart"),
    path("update-cart/", views.update_from_cart,name="update-cart"),
    
    
    path("checkout/<oid>/", views.checkout,name="checkout"),
    
    path("paypal/", include('paypal.standard.ipn.urls')),
    
    path("payment-completed/<oid>", views.payment_completed_view,name="payment-completed"),
    # path("payment-completed/", views.payment_completed_view,name="payment-completed"),
    
    path("payment-failed/", views.payment_failed_view,name="payment-failed"),
    
    
    path("dashboard/", views.customer_dashboard,name="dashboard"),
    
    path("dashboard/order/<int:id>", views.order_detail,name="order-detail"),
    
    path("make-default-address", views.make_address_default,name="make-default-address"),
    
    path("wishlist/", views.wishlist_view,name="wishlist"),
    path("add-to-wishlist/",views.add_to_wishlist,name="add-to-wishlist"),
    path("remove-from-wishlist/",views.remove_wishlist,name="remove-from-wishlist"),

    
    path("contact/",views.contact,name="contact"),
    path("ajax-contact-form/",views.ajax_contact_form,name="ajax_contact"),
    
    
    
    path("save_checkout_info/",views.save_checkout_info, name="save-checkout-info"),
    
    path("api/create_checkout_session/<oid>/", views.create_checkout_session,name="create_checkout_session")

    
]
