from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('main/', views.main, name = "main"),
    path('redirect/', views.helper, name = "helper"),
    path('cart/', views.cart, name = 'cart'),
    path('redirectS/', views.helperS, name = 'helperS'),
    path('thankyou/', views.checkout, name = 'checkout'),
    path('admin/', views.admin, name = 'admin'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('profile/', views.profile, name = 'profile'),
    path('update/', views.update, name = 'update') # why not a javascript function that updates the cookie and redirects? why a post form
 ]