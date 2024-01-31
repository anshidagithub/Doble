from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from category.views import _cart_id
from category.models import cart,cartitem


from django.contrib import messages

# Create your views here.

def loginn(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminpanel:dashbord')
        else:
            return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_superuser:
                try:
                    
                    cartt = cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = cartitem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        print(is_cart_item_exists)
                        cart_item = cartitem.objects.filter(cart=cartt)

                        for item in cart_item:
                            item.user= user
                            item.save()
                except:
                    pass
                  
                login(request, user)
                return redirect('adminpanel:dashbord')
            else:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Email or password is incorrect!!')
            return redirect('loginn')

    return render(request, 'login.html')
def signup(request):
  if request.user.is_authenticated:
      if request.user.is_superuser:
       return redirect('adminpanel:dashbord')
      else:
       return redirect('home')
    
  if request.method == 'POST':
          firstname = request.POST['firstname']
          lastname = request.POST['lastname']
          phone = request.POST['phone_number']
          email = request.POST['email']
          password1 = request.POST['password1']
          password2 = request.POST['password2']
          if password1 == password2:
            
              if CustomUser.objects.filter(phone=phone).exists():
                  messages.error(request, 'phon already taken!!')
                  return redirect('signup')
              
              elif CustomUser.objects.filter(email=email).exists():
                  messages.error(request, 'email already taken!!')
                  return redirect('signup')
              
              else:
                  user = CustomUser.objects.create_user(first_name=firstname,last_name=lastname,email=email,password=password1,phone=phone)
                  user.save()
                  return redirect('loginn')
          else:
              messages.error(request, 'password do not maching!!')
              return redirect('signup')
                
  return render(request,'registration.html')

def logout(request):
    
    if request.user.is_authenticated:
        request.session.flush()
        return redirect('loginn')
    




