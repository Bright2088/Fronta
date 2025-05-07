# from zoneinfo import available_timezones
from django.shortcuts import render
from django.db.models import Q
from .models import *

from django.shortcuts import redirect
from .models import Product
# from .cart import Cart
from .models import Cart, Product, CartItem
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from base import views as base_views


def home(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)


    if query:
        products = products.filter( Q(name__icontains=query) | Q(description__icontains=query))
    context = {
        "categories": categories,
        "products" : products,
    }
    return render(request, "base/home.html", context)

def whatnew(request):
    return render(request, "base/what_new.html")


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(available=True)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, "base/category_detail.html", context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    context = {
        'product': product,
    }
    return render(request, 'base/product_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_item = cart.items.filter(product_id=product_id).first()
        if cart_item:
            cart_item.delete()
    return redirect('cart_detail')

# @login_required
# def cart_detail(request):
#     cart = Cart.objects.filter(user=request.user).first()
#     items = cart.items.all() if cart else []
#     total = sum(item.get_total_price() for item in items)

#     return render(request, 'base/cart_detail.html', {
#         'cart': cart,
#         'items': items,
#         'total': total,
#     })

def cart_detail(request):
    if not request.user.is_authenticated:
        return redirect('login')  # or use 'signin' if that's your login URL name

    cart = Cart.objects.filter(user=request.user).first()
    items = cart.items.all() if cart else []
    total = sum(item.quantity * item.product.price for item in items)

    return render(request, 'base/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })
@login_required
def update_cart_item(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    if cart and request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = cart.items.filter(product_id=product_id).first()
        if cart_item:
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('cart_detail')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


