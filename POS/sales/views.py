from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, SaleForm, CustomerForm, SaleProductFormset 
from .models import Product, Sale, SaleProduct, Customer
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.urls import reverse_lazy

def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'sales/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
                form = ProductForm()
    return render(request, 'sales/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'sales/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'sales/product_confirm_delete.html', {'product': product})



def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})

def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'sales/sale_list.html', {'sales': sales})


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['name', 'email']
    success_url = reverse_lazy('customer_list') 

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'sales/customer_detail.html', {'customer': customer})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, 'sales/customer_form.html', {'form': form, 'form_title': 'New Customer', 'form_button_text': 'Create'})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'sales/customer_form.html', {'form': form, 'form_title': 'Edit Customer', 'form_button_text': 'Save'})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'sales/customer_confirm_delete.html', {'customer': customer})



class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sale_list')

    def form_valid(self, form):
        # Save the Sale instance
        sale = form.save(commit=False)
        sale.save()

        # Add SaleProduct instances for each selected product
        for product in form.cleaned_data['products']:
            quantity = form.cleaned_data['quantities'][str(product.id)]
            SaleProduct.objects.create(sale=sale, product=product, quantity=quantity)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_form'] = CustomerForm()
        context['product_formset'] = SaleProductFormset(queryset=Product.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        product_formset = SaleProductFormset(request.POST)

        if form.is_valid() and product_formset.is_valid():
            return self.form_valid(form, product_formset)
        else:
            return self.form_invalid(form, product_formset)

            
        
        
        
        

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'

    def post(self, request, *args, **kwargs):
        sale = self.get_object()
        sale.complete_sale()
        return redirect('sale_detail', pk=sale.pk)
