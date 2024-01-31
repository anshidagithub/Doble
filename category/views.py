from django.shortcuts import render,redirect
from category.models import category,subcategory,product,cart,cartitem
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    

def add_cart(request,product_id):
    
    productt = product.objects.get(id=product_id) #get the product
    
    try:
       cartt= cart.objects.get(cart_id= _cart_id(request))
    except cart.DoesNotExist:
         cartt= cart.objects.create(
         cart_id= _cart_id(request)
                )
         cartt.save()

    try:
      cart_item= cartitem.objects.get(product=productt ,cart=cartt)
      cart_item.quantity += 1
    except cartitem.DoesNotExist:
       cart_item= cartitem.objects.create(
          product=productt,
          quantity= 1,
            cart= cartt,
            )
    cart_item.save()
            
    return redirect('cartpage')

def remove_cart(request,product_id):
        cartt = cart.objects.get(cart_id = _cart_id(request)) 
        productt = get_object_or_404(product,id=product_id)
        cart_item =cartitem.objects.get(product=productt,cart=cartt,)
        
            
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        
        else:
            cart_item.delete()
        
        return redirect('cartpage') 


def remove_cart_item(request,product_id):
    cartt = cart.objects.get(cart_id = _cart_id(request)) 
    productt = get_object_or_404(product,id=product_id)
    cart_item =cartitem.objects.get(product=productt,cart=cartt,)
    cart_item.delete()
    return redirect('cartpage') 



 

def cartpage(request,total=0, quantity=0, cart_items=None):


 try:
    tax=0
    grand_total=0
    if request.user.is_authenticated:
            cart_items = cartitem.objects.filter(user=request.user,is_active=True)
    else:
        cartt= cart.objects.get(cart_id= _cart_id(request))
        cart_items= cartitem.objects.filter(cart=cartt,is_active=True)
    for cart_item in cart_items:
        total +=(cart_item.product.price* cart_item.quantity)
        quantity+= cart_item.quantity
        tax =(2 * total)/100
        grand_total = total + tax 

 except :
        pass #just ignoe
 context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax' : tax,
        'grand_total': grand_total
        
    }
      
    
 return render(request,'cart.html',context)

@login_required(login_url='login')
def checkout(request,total=0, quantity=0, cart_items=None):
        
    try:
        tax=0
        grand_total=0
        cartt= cart.objects.get(cart_id= _cart_id(request))
        cart_items= cartitem.objects.filter(cart=cartt,is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price* cart_item.quantity)
            quantity+= cart_item.quantity
            tax =(2 * total)/100
            grand_total = total + tax 

    except :
            pass #just ignoe
    context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax' : tax,
            'grand_total': grand_total
            
        }
    return render(request,'checkout.html',context)