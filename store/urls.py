from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='store-home'),
    path('cart/', views.cart, name='cart'),
    path('shop/', views.shop, name='shop'),
    path('checkout/', views.checkout, name='checkout'),
    path('faq/', views.faq, name='faq'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('about-us/', views.about_us, name='about-us'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('return-policy/', views.return_policy, name='return-policy'),
    path('terms-conditions/', views.terms_conditions, name='terms-conditions'),
    path('product-details/', views.product_details, name='product-details'),
    path('terms-of-use/', views.terms_of_use, name='terms-of-use'),
    path('sales-refunds/', views.sales_refunds, name='sales-refunds'),
    
]
