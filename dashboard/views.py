import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User

# Create your views here.

@login_required
def index(request):
    staff_orders = Order.objects.all().filter(staff=request.user).order_by('-id')
    orders = Order.objects.all().order_by('-id')
    products = Product.objects.all().order_by('-id')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.staff = request.user
            order.save()
            return redirect('dashboard:index')
    else:
        form = OrderForm()

    context = {
        'staff_orders': staff_orders,
        'orders': orders,
        'products': products,
        'form': form,
        'workers': User.objects.all()
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def staff(request):
    workers = User.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    context = {
        'workers': workers,
        'products': products,
        'orders': orders
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, pk):
    worker = User.objects.get(pk=pk)
    context = {
        'worker': worker 
    }
    return render(request, 'dashboard/staff_detail.html', context)

@login_required
def product(request):
    products = Product.objects.order_by('-id').all()
    workers = User.objects.all()
    orders = Order.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added sucessfully!')
            return redirect('dashboard:product')
    else:
        form = ProductForm()

    context = {
        'products': products,
        'form': form,
        'workers': workers,
        'orders': orders
    }
    return render(request, 'dashboard/product.html', context)

@login_required
def delete_product(request, pk):
    item = Product.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.info(request, 'Product deleted successfully!')
        return redirect('dashboard:product')
    return render(request, 'dashboard/delete_product.html')

@login_required
def update_product(request, pk):
    item = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('dashboard:product')
    else:
        form = ProductForm(instance=item)
    context = {
        'form':form
    }
    return render(request, 'dashboard/update_product.html', context)


@login_required
def order(request):
    orders = Order.objects.all().order_by('-id')
    workers = User.objects.all()
    products = Product.objects.all()
    context = {
        'orders': orders,
        'workers': workers,
        'products': products
    }
    return render(request, 'dashboard/order.html', context)