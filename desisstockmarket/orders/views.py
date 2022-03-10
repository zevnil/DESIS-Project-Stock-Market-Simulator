from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Order
from .forms import OrderForm
from stocks.models import Stock
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.

# Home page of stocks displays list of all stocks that are available and can be traded
# on our platform.

# Home page shall show you all the orders by this user
# TODO: Change it for particular user after adding user


@login_required(login_url='base:login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # TODO: Later we shall filter out only the top 10 or so stocks to show here in home of orders
    stocks = Stock.objects.all()
    orders = Order.objects.filter(
        Q(user=request.user) &
        (Q(stock__stockName__icontains=q) |
         Q(stock__fullCompanyName__icontains=q)))
    # .order_by('-updatedAt')

    orders_count = orders.count()
    context = {'orders': orders, 'stocks': stocks,
               'orders_count': orders_count}
    return render(request, 'orders/home.html', context)

# Info about each individual stock


# def info(request, id):
#     stock = Stock.objects.get(stockId=id)
#     context = {'stock': stock}
#     return render(request, 'stocks/info.html', context)

@login_required(login_url='base:login')
def createOrder(request):
    form = OrderForm()

    # Post route is hit after user has submitted their details
    if request.method == "POST":
        print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            # If the data received via the form is valid, we save it to the DB
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            # After form has been saved, we just redirect back to home page
            return redirect('orders:home')

    context = {"form": form}
    return render(request, 'orders/order_form.html', context)


@login_required(login_url='base:login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.updatedAt = datetime.now()
            # order.save(update_fields=['updatedAt'])
            order.save()
            # TODO: The sorting of orders isn't working correctly. If I update an order
            # then it should come on the top of the list, which isnt happening currently.
            return redirect('orders:home')

    context = {'form': form}
    return render(request, 'orders/order_form.html', context)


@login_required(login_url='base:login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    # If its a POST request, means that the user submitted the form, and hence we shall delete
    if request.method == "POST":
        order.delete()
        return redirect('orders:home')

    context = {'obj': order}
    return render(request, 'orders/delete.html', context)
