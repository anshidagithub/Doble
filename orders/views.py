from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from category.models import cartitem, product
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import datetime
import json
from userprofile.models import Address,UserProfile


# Create your views here.

def payments(request):
    body = json.loads(request.body)
    #store transaction deatails inside payment model
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    paymentt= Payment(
        user = request.user,
        payment_id = body['transID'],
        order_id = order.order_number,
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    paymentt.save()

    order.payment = paymentt
    order.is_ordered = True
    order.save()

    # move cartitems to order product table
    cartitems= cartitem.objects.filter(user= request.user)

    for item in cartitems:
        orderproduct= OrderProduct() 
        orderproduct.order_id= order.id
        orderproduct.payment= paymentt
        orderproduct.user_id= request.user.id
        orderproduct.product_id= item.product_id
        orderproduct.quantity= item.quantity
        orderproduct.product_price= item.product.price
        orderproduct.ordered= True
        orderproduct.save()

        # Reduce quantity of product
        productt =  product.objects.get( id = item.product_id)
        productt.stock -= item.quantity
        productt.save()

    
    # clear cart
    cartitem.objects.filter(user=request.user).delete()

      # send order number transaction id back to send data method via jsonResponce
    data = {
        'order_number':order.order_number,
        'transID':paymentt.payment_id
    }
    print('boss')
    return JsonResponse(data)


   

def place_order(request, total=0, quantity=0):
    print('helooo')
    current_user = request.user
    print(current_user, 'current user')
    # if the cart count is less than or equal to 0, then redirect back to the category
    cart_items = cartitem.objects.filter(user=current_user)
    print(cart_items,'cartitem')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('category')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax 
   

    data = None  # Initialize the data variable
    
    if request.method == 'POST':
    
        id = request.POST['flexRadioDefault']
        address  = Address.objects.get(user = request.user,id = id)
        data = Order()
        data.user = current_user
        data.first_name = address.first_name
        data.last_name = address.last_name
        data.phone = address.phone
        data.email = address.email
        data.address_line_1 = address.address_line1
        data.address_line_2 = address.address_line2
        data.state = address.state
        data.city = address.city
        data.country = address.country
        data.order_note = address.order_note
        data.order_total = grand_total
        data.tax = tax 
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        # Generate order number if data is not None
        if data:
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order= Order.objects.get(user= current_user, is_ordered= False, order_number= order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total
            }

        return render(request,'payments.html',context )
    else:
        return redirect('checkout')
    
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    print(transID, "testing transid")
    try:
        print('jis')
        order = Order.objects.get(order_number=order_number)
        print('lofi')
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        print('break')
        # payment = Payment.objects.get(payment_id=transID)
        print('mallayya')
        total = 0
        for i in ordered_products:
            total += i.product_price * i.quantity
        tax = (2*total)/100
        
        print('check')
        grand_total = total + tax 
        payment = Payment.objects.get(payment_id=transID)
        context={
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'total':total,
            'tax':tax,
            
        }
        return render(request,'order_complete.html',context)
    
    except(payment.DoesNotExist, order.DoesNotExist):
        return redirect('home')
    


def cash_on_delivery(request,id):
   print('anshiiiiii')
   # Move cart item to ordered product table
   try:
      
      order = Order.objects.get(user=request.user,is_ordered=False,order_number=id)
      cart_items =cartitem.objects.filter(user=request.user)
      order.is_ordered = True
      total = 0
      for i in cart_items:
           total += i.product.price * i.quantity
      tax = (2*total)/100
      shipping = (2*total)/100
      grand_total = order.order_total + shipping
      order.order_total = grand_total
      order.save()

      payment = Payment(
         user = request.user,
         payment_id = order.order_number,
         order_id = order.order_number,
         payment_method = 'Cash on Delivery',
         amount_paid = order.order_total,
         status = False
      )
      payment.save()
      order.payment = payment
      order.is_ordered = True
      order.save()
      print('dill')
      
      for cart_item in cart_items:
         order_product = OrderProduct()
         order_product.order_id = order.id
         order_product.payment = payment
         order_product.user_id = request.user.id
         order_product.product_id = cart_item.product_id
         order_product.quantity = cart_item.quantity
         order_product.product_price = cart_item.product.price
         order_product.ordered = True
         print('les')
         print(order_product.order_id)
         order_product.save()

         cart_item = cartitem.objects.get(id=cart_item.id)
         
         
         order_product = OrderProduct.objects.get(id=order_product.id)
         print('heeeeeeeeeeeeeeeee')
         order_product.save()

         # Reduce quantity of product
         productt = product.objects.get( id = cart_item.product_id)
         productt.stock -= cart_item.quantity
         productt.save()


         #clear cart
         print('lala')
      cartitem.objects.filter(user= request.user).delete()

      ordered_products = OrderProduct.objects.filter(order_id = order.id)
      context ={
            'order':order,
            'ordered_products':ordered_products,
            'payment':payment,
            'total':total,
            'tax':tax,
            'shipping':shipping,
            
            
         }  
      return render(request,'succes.html',context) 
   except Exception as e:
      print(e)
      return redirect('home')
      


def wallet(request,id):
   print('hlo')
   try:
      print('hoi')
      order = Order.objects.get(user=request.user,is_ordered=False,order_number=id)
      cart_items = cartitem.objects.filter(user=request.user)
      order.is_ordered = True
      payment = Payment(
               user = request.user,
               payment_id = order.order_number,
               order_id = order.order_number,
               payment_method = 'Wallet payment', 
               amount_paid = order.order_total,
               status = 'True'
      )
      payment.save()
      order.payment = payment
      order.is_ordered = True
      order.save()

      # Move cart item to ordered product table
      for item in cart_items:
         order_product = OrderProduct()
         order_product.order_id = order.id
         order_product.payment = payment
         order_product.user_id = request.user.id
         order_product.product_id = item.product_id
         order_product.quantity = item.quantity
         order_product.product_price = item.product.price
         order_product.ordered = True
         order_product.save()

         cart_item = cartitem.objects.get(id=item.id)
         
         # Reduce quantity of product
         productt = product.objects.get( id = cart_item.product_id)
         productt.stock -= cart_item.quantity
         productt.save()

         

      cartitem.objects.filter(user= request.user).delete()       
      ordered_products = OrderProduct.objects.filter(order_id = order.id)  
      total = 0
      for i in ordered_products:
           total += i.product_price * i.quantity
      tax = (2*total)/100  
      profile = UserProfile.objects.get(user=request.user)  
      profile.wallet -= order.order_total
      profile.save() 
      print('ann')
      
      context ={
            'order':order,
            'ordered_products':ordered_products,
            'payment':payment,
            'total':total,
            'tax':tax, 
            'profile':profile,     
         }  
      return render(request,'wallet_success.html',context)   


   except Exception as e:
     print(e)
       
 
     print('potti')
   return redirect('home')

