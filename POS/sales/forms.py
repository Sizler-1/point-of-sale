from django import forms
from .models import Product, Sale, Customer, SaleProduct
from django.forms.models import inlineformset_factory


class SaleProductForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = ['product', 'quantity']

SaleProductFormset = inlineformset_factory(Sale, SaleProduct, form=SaleProductForm, extra=1, can_delete=False)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('code', 'name', 'price', 'quantity')


class SaleForm(forms.ModelForm):
    product_quantities = forms.CharField()

    class Meta:
        model = Sale
        fields = ['customer', 'payment_type', 'product_quantities']

    def clean(self):
        cleaned_data = super().clean()
        product_quantities = cleaned_data.get('product_quantities')
        if product_quantities:
            product_ids, quantities = [], []
            for pq in product_quantities.split(';'):
                pid, qty = pq.split(':')
                product_ids.append(int(pid))
                quantities.append(int(qty))
            products = Product.objects.filter(id__in=product_ids)
            if len(products) != len(quantities):
                raise forms.ValidationError("Invalid product quantities.")
            cleaned_data['products'] = products
            cleaned_data['quantities'] = quantities
        else:
            raise forms.ValidationError("Product quantities required.")
        return cleaned_data
