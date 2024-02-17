from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order,OrderProduct,Payment
from .models import UserProfile,Address
from .forms import CustomUserForm,UserProfileForm,AddressForm
from django.contrib import messages
from account.models import CustomUser
from category.models import product

# Create your views here.
@login_required(login_url='loginn')
def userdash(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    user=request.user
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context={
        'orders_count':orders_count,
        'user':user,
        'userprofile':userprofile 
    }
    return render(request,'userdash.html',context)

@login_required(login_url='loginn')
def my_orders(request):
    orders= Order.objects.order_by('-created_at').filter(user=request.user, is_ordered=True)
    context= {
        'orders' :orders
    }
    return render(request,'my_orders.html',context)

@login_required(login_url='loginn')
def order_details(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    orders = Order.objects.get(order_number=order_id)
    total=0
    for i in order_detail:
           total += i.product_price * i.quantity
    tax = (2*total)/100
    shipping = (2*total)/100
    print('check')
    
    
    context = {
        'order_detail':order_detail,
        'order':orders,
        'total':total,
        'tax':tax,
        'shipping':shipping,
       
    }

    return render(request,'order_details.html',context)

@login_required(login_url='loginn')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
        else:
            return redirect('edit_profile')
    else:
        user_form = CustomUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context= {
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
        }

    return render(request,'edit_profile.html', context)

@login_required(login_url='loginn')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = CustomUser.objects.get(email__exact=request.user.email)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                #auth.logout(request)
                messages.success(request,'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request,'Password does not match!')
            return redirect('change_password')

    return render(request, 'change_password.html')

@login_required(login_url='loginn')
def myAddress(request):
  current_user = request.user
  address = Address.objects.filter(user=current_user)
  
  context = {
    'address':address,
  }
  return render(request,'myAddress.html', context)

@login_required(login_url='loginn')
def addAddress(request):
        if request.method == 'POST':
            form = AddressForm(request.POST,request.FILES,)
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
                return redirect('myAddress')
            else:
                messages.success(request,'Form is Not valid')
                return redirect('myAddress')
        else:
            form = AddressForm()
            context={
                'form':form
            }    

        return render(request,'addAddress.html',context)

@login_required(login_url='loginn')
def editAddress(request, id):
  address = Address.objects.get(id=id)
  if request.method == 'POST':
    form = AddressForm(request.POST, instance=address)
    if form.is_valid():
      form.save()
      messages.success(request , 'Address Updated Successfully')
      return redirect('myAddress')
    else:
      messages.error(request , 'Invalid Inputs!!!')
      return redirect('myAddress')
  else:
      form = AddressForm(instance=address)
      
  context = {
            'form' : form,
        }
  return render(request , 'editAddress.html' , context)

@login_required(login_url='loginn')
def deleteAddress(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('myAddress')




def cancel_order(request, order_number):
    if request.user.is_superuser:
        order = get_object_or_404(Order, order_number=order_number)
    else:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)

    order.status = "Cancelled"
    order.save()

    # Use get_object_or_404 to retrieve the Payment object
    payment = get_object_or_404(Payment, order_id=order.order_number)

    order_products = OrderProduct.objects.filter(user=request.user, order=order)

    for order_product in order_products:
        product_instance = order_product.product
        product_instance.stock += order_product.quantity
        product_instance.save()

    profile = UserProfile.objects.get(user=request.user)

    if payment.status in ['COMPLETED','True']:  # Access payment status and amount_paid using the payment instance
        profile.wallet += payment.amount_paid
        profile.save()

    payment.delete()

    if request.user.is_superuser:
        messages.success(request, f"{profile.user.first_name} cancelled {order.order_number}")
        return redirect('orders')
    else:
        messages.success(request, 'Item cancelled successfully')
        return redirect('my_orders')
    
    
def return_order(request,order_number):
  if request.method == 'POST':
   return_reason = request.POST['return_reason']
  order = Order.objects.get(order_number = order_number,user = request.user)
  order.status = "Returned"
  order.is_returned = True
  order.return_reason = return_reason
  order.save()
  payment = Payment.objects.get(order_id = order.order_number)
  

  order_products = OrderProduct.objects.filter(user=request.user,order=order)
  for order_product in order_products: 
         # increase quantity of product
         productt = product.objects.get( id = order_product.product_id)
         productt.stock += order_product.quantity
         productt.save()
  
        

  profile = UserProfile.objects.get(user=request.user) 
  if payment.status == 'True':
       print(payment.amount_paid)
       profile.wallet += payment.amount_paid
       print(profile.wallet)
       profile.save() 

  payment.delete()              
  messages.success(request,'item returned successfully')
  return redirect('my_orders')

       
