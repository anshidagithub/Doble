from django.shortcuts import render,redirect
from category.models import category,subcategory,product,cart,cartitem
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import uuid
from userprofile.models import Address
from userprofile.forms import AddressForm
from django.contrib import messages
# Create your views here.

def _cart_id(request, user=None):
    if user and user.is_authenticated:
        # Use the user's ID as part of the cart identifier for authenticated users
        return f"user_{user.id}"
    else:
        cart = request.session.get('cart_id')
        if not cart:
            # If no cart_id exists in the session, create a new one
            cart = f"guest_{uuid.uuid4().hex[:5]}"
            request.session['cart_id'] = cart

        return cart

def add_cart(request, product_id):
    current_user = request.user

    try:
        productt = product.objects.get(id=product_id)
    except product.DoesNotExist:
        # Handle the case where the product does not exist
        return redirect('cartpage')

    if current_user.is_authenticated:
        cart_id = _cart_id(request, user=current_user)
    else:
        cart_id = _cart_id(request)

    try:
        cart_instance = cart.objects.get(cart_id=cart_id)
    except cart.DoesNotExist:
        cart_instance = cart.objects.create(cart_id=cart_id, user=current_user if current_user.is_authenticated else None)
        cart_instance.save()

    is_cart_item_exists = cartitem.objects.filter(product=productt, cart=cart_instance, user=current_user if current_user.is_authenticated else None).exists()
    if is_cart_item_exists:
        cart_item = cartitem.objects.get(product=productt, cart=cart_instance, user=current_user if current_user.is_authenticated else None)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = cartitem.objects.create(product=productt, quantity=1, cart=cart_instance, user=current_user if current_user.is_authenticated else None)

    return redirect('cartpage')

def remove_cart(request,product_id,cart_item_id):
    
    productt = get_object_or_404(product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item =cartitem.objects.get(product=productt,user=request.user,id=cart_item_id)
        else:
            cartt = cart.objects.get(cart_id = _cart_id(request))    
            cart_item =cartitem.objects.get(product=productt,cart=cartt,id=cart_item_id)
        if cart_item.quantity > 1:
          cart_item.quantity -= 1
          cart_item.save()
    
        else:
          cart_item.delete()
    except:
        pass
    return redirect('cartpage')  

def remove_cart_item(request,product_id,cart_item_id):
    productt = get_object_or_404(product,id=product_id)
    if request.user.is_authenticated:
        cart_item = cartitem.objects.get(product=productt,user=request.user,id=cart_item_id)
    else:
        cartt = cart.objects.get(cart_id= _cart_id(request))
        cart_item = cartitem.objects.get(product=productt,cart=cartt,id=cart_item_id)
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

@login_required(login_url='loginn')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = None
    grand_total = None
    address = Address.objects.filter(user = request.user)
    form = AddressForm()
    

    try:
        if request.user.is_authenticated:
            cart_items = cartitem.objects.filter(user=request.user, is_active=True)
        else:
            cartt = cart.objects.get(cart_id=_cart_id(request))
            cart_items = cartitem.objects.filter(cart=cartt, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax    
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'address':address,
        'form':form,
       
    }

    return render(request, 'checkout.html', context)


def deleteCheckoutAddress(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('checkout')


def AddCheckoutAddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line1 =  form.cleaned_data['address_line1']
            detail.address_line2  = form.cleaned_data['address_line2']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.save()
            messages.success(request,'Address added Successfully')
            return redirect('checkout')
        else:
            messages.error(request,'Form is Not valid')
            return redirect('checkout')
  