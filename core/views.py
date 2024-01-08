from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt 
from .utils import *

from .models import *

def store(request):
    data = Cart(request)
    cart_items = data["cart_items"]

    products = Product.objects.all()
    return render(request,"core/store.html",{
        "products":products,
        'cart_items':cart_items,
    })

def checkout(request):
   
    data = Cart(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    
    return render(request,"core/checkout.html",{
        "items":items,
        "order":order,
        "cart_items":cart_items
    })
    
def cart(request):

    data = Cart(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
       
    return render(request,"core/cart.html",{
        "items":items,
        "order":order,
        "cart_items":cart_items
    })

def update_item(request):

    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('product id', productID)
    print('action', action)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order,created = Order.objects.get_or_create(customer=customer, complete = False)
    orderitem,created = OrderItem.objects.get_or_create(order = order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('item is added', safe=False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer  = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete = False)

    else:
       customer,order = guestOrder(request, data)
            
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
            )

    return JsonResponse('payment completed!', safe=False)

def signin(request):
    if request.user.is_authenticated:
        messages.info(request, "user already logged in")
        return redirect("store")

    else:
        if request.method=="POST":
           username = request.POST["username"]
           password = request.POST["password"]

           user = auth.authenticate(request,username=username,password=password)
           if user is not None:
              auth.login(request,user)
              return redirect("/")
           else:
              return HttpResponse("username or password is incorrect!")
        else:
            return render(request, "core/signin.html")


def signup(request):
    if request.user.is_authenticated:
        messages.info(request, "user already logged in")
        return redirect("store")

    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('signup')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    user_login = auth.authenticate(username=username, password=password1)
                    auth.login(request, user_login)
                    return redirect("store")
            else:
                messages.info(request, 'Password Not Matching')
                return redirect('signup')
        else:
            return render(request, 'core/signup.html')
@login_required
def logoutPage(request):
    logout(request)
    return redirect("signin")