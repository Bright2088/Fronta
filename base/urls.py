from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
from base import views as base_views
# from fronta.base import views

urlpatterns = [
    path('', views.home, name="home"),   
    path('what_new/', views.whatnew, name="whatnew"),   
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    path('cart/', views.cart_detail, name="cart_detail"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_item, name='update_cart_item'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', base_views.signup_view, name='signup'),
  
]
