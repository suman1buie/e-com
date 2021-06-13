import json
from django.shortcuts import redirect, render
from .models import *
from django.http import JsonResponse
import datetime
from django.contrib.auth.models import User ,auth
from django.contrib.auth import authenticate
from django.contrib import messages

def cart(request):
    total = 0
    if request.user.is_authenticated:
        castomer = request.user.castomer
        order,created = Order.objects.get_or_create(coustomer=castomer,competed = False)
        cartItems = order.get_cart_items
        allItem = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])

        except:
            cart={}

        allItem = []
        order = {'get_cart_items':0,'get_cart_total':0 , 'shipping':False}
        cartItems = order['get_cart_items']
        for c in cart:
            try:
                product = Product.objects.get(id=c)
                
                cartItems+=cart[c]['quantity']
                total = ( product.price * cart[c]['quantity'])
                order['get_cart_items'] +=cart[c]['quantity']
                order['get_cart_total'] += total
                
                item = {
                    'Product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'image':product.image
                    },
                    'quantity':cart[c]['quantity'],
                    'get_total':total
                }
                allItem.append(item)
                if product.digital == False:
                    order['shipping'] = True
            except:
                pass
    return render(request,"store/cart.html",{"items":allItem,"order":order , 'cartItems':cartItems})



def store(request):
    if request.user.is_authenticated:
        castomer = request.user.castomer
        order,created = Order.objects.get_or_create(coustomer=castomer,competed = False)
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}

        order = {'get_cart_items':0}
        cartItems = order['get_cart_items']
        for c in cart:
            cartItems+=cart[c]['quantity']
    products = Product.objects.all()
    context = {"products": products , 'cartItems':cartItems}
    return render(request,"store/store.html",context)



def checkout(request):
    if request.user.is_authenticated:
        castomer = request.user.castomer
        order,created = Order.objects.get_or_create(coustomer=castomer,competed = False)
        allItem = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
            
        allItem = []
        order = {'get_cart_items':0,'get_cart_total':0 , 'shipping':False}
        cartItems = 0
        cartItems = order['get_cart_items']
        for c in cart:
            product = Product.objects.get(id=c)
            
            cartItems+=cart[c]['quantity']
            total = ( product.price * cart[c]['quantity'])
            order['get_cart_items'] +=cart[c]['quantity']
            order['get_cart_total'] += total
            
            item = {
                'Product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image
                },
                'quantity':cart[c]['quantity'],
                'get_total':total
            }
            allItem.append(item)    
    
    return render(request,"store/checkout.html",{"items":allItem,"order":order,'cartItems':cartItems})

 
def updateItem(request):
    data = json.loads(request.body)
    pId = data['pId']
    action = data['action']
    castomer = request.user.castomer
    product = Product.objects.get(id=pId)
    order, created = Order.objects.get_or_create(coustomer=castomer,competed=False )
    orderItem, created = OrderItem.objects.get_or_create(order=order, Product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item is added', safe=False)


def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        castomer = request.user.castomer
        order, created = Order.objects.get_or_create(coustomer=castomer,competed=False )

    else:
        # print("User not loged in!!")
        print("cookies : ",request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
            
        allItem = []
        order = {'get_cart_items':0,'get_cart_total':0 , 'shipping':False}
        cartItems = 0
        cartItems = order['get_cart_items']
        for c in cart:
            product = Product.objects.get(id=c)
            cartItems+=cart[c]['quantity']
            total = ( product.price * cart[c]['quantity'])
            order['get_cart_items'] +=cart[c]['quantity']
            order['get_cart_total'] += total
            
            item = {
                'Product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image
                },
                'quantity':cart[c]['quantity'],
                'get_total':total
            }
            allItem.append(item)    
        items = allItem
        castomer ,created = Castomer.objects.get_or_create(
            email = email
        )       
        castomer.name = name
        castomer.save()
        order = Order.objects.create(
            coustomer = castomer,
            competed = False,
        )
        for item in items:
            product = Product.objects.get(id=item['Product']['id'])
            orderItem = OrderItem.objects.create(
                Product = product,
                order = order,
                quantity = item['quantity']
            )

    total = float(data['form']['total'])   
    order.transation_id = transaction_id
        
    if total == order.get_cart_total:
        order.competed = True
        
    order.save()
    # print("here->>>>>>>>>>")
    print(data)
    if order.shipping == True:
        ShippingAddress.objects.create(
            castomer = castomer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )                 
    return JsonResponse("Pyement submited", safe=False)


def login(request):
    if request.method == 'POST':
        username     = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You loged In successfully!!!")
            return redirect('/')
        else:
            messages.error(request,"invalid username or password")
            return redirect('/login')
    
    return render(request,'store/login.html',{})


def register(request):
    if request.method == 'POST':
        username     = request.POST['username']
        email     = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email Allredy Register.. !!Try new One..!")
            return redirect('/registers')
        else:
            user = User.objects.create_user(username, email, password)
            user.save()
            new_castomar = Castomer.objects.create(User=user,name=username,email=email)
            new_castomar.save()
            saddress = ShippingAddress.objects.create(castomer=new_castomar,address=address,city=city,state=state,zipcode=zip)
            saddress.save()
            messages.success(request,"Account create successfully! :)\n Now Log In")
            return redirect('/login')
    return render(request,'store/registration.html',{})


def log_out(request):
	auth.logout(request)
	messages.success(request,"You Loged Out Successfully !")
	return redirect('/')

# env\Scripts\activate