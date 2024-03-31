from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('main/', views.main, name = "main"),
    path('helper/', views.helper, name = "helper"),
    path('cart/', views.cart, name = 'cart'),
 ]