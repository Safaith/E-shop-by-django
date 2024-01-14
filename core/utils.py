import json
from .models import *
from django.contrib.auth.models import User

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    # print('cart: ',cart)
    items = []
    order = {"get_cart_items":0,"get_cart_total":0,"shipping":False}
    cart_items = order['get_cart_items']

    for i in cart:
        try:
            cart_items += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)

            if product.is_digital == False:
                order['shipping'] = True
        except:
            pass
    return {"items":items, "order":order, "cart_items":cart_items}

def Cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cart_items =order.get_cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cart_items = cookieData['cart_items']
    return {"items":items, "order":order, "cart_items":cart_items}

def guestOrder(request, data):
    print("user is not logged in")
    name = data['form']['name']
    email = data['form']['email']
    password = data['form']['password']
    User.objects.create_user(username=name, email=email, password=password)

    cookiedata = cookieCart(request)
    items = cookiedata['items']

    customer,created = Customer.objects.get_or_create(email=email)
    customer.name =name
    customer.save()
    
    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        
        orderitem = OrderItem.objects.create(product=product,order=order, quantity=item['quantity']) 

    return customer,order   
