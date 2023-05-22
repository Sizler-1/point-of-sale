from django.contrib import admin
from .models import Customer, Product, Sale, SaleProduct

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(SaleProduct)



