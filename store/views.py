from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def cart(request):
    return render(request, 'cart.html')

def shop(request):
    return render(request, 'shop.html')

def contact_us(request):
    return render(request, 'contact.html')

def about_us(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')

def product_details(request):
    return render(request, 'product_details.html')

def return_policy(request):
    return render(request, 'return.html')

def privacy_policy(request):
    return render(request, 'policy.html')

def faq(request):
    return render(request, 'faq.html')

def terms_conditions(request):
    return render(request, 'terms_conditions.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def sales_refunds(request):
    return render(request, 'sales-refunds.html')