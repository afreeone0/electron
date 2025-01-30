from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def make_order(request):
    context = {
        'title': 'Order'
    }
    return render(request, 'orders/make_order.html', context=context)


@login_required(login_url='login')
def orders_archive(request):
    context = {
        'title': 'Orders archive'
    }
    return render(request, 'orders/orders_archive.html', context=context)
