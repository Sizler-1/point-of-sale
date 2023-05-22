from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, through='SaleProduct')
    date_created = models.DateTimeField(auto_now_add=True)

    def complete_sale(self):
        for sale_product in self.saleproduct_set.all():
            sale_product.product.quantity -= sale_product.quantity
            sale_product.product.save()
        self.completed = True
        self.save()


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
