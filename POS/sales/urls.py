from django.urls import path

from . import views
from .views import CustomerCreateView


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('sale/create/', views.SaleCreateView.as_view(), name='sale_create'),

    
]
