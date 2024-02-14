from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from account.models import CustomUser
from category.models import category,subcategory,product
from orders.models import Payment 
from django.db.models import Q
from orders.models import Order
from django.contrib import messages
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.

def dashbord(request):
    
     return render(request,'dashbord.html')
    
   


def userslist(request):
    users= CustomUser.objects.all()
    paginator = Paginator(users,8)
    page= request.GET.get('page')
    paged_users = paginator.get_page(page)
    dict_users={
        'users': paged_users
        }
    return render(request,'User.html',dict_users)
    
    


def  toggle_user_status(request,user_id):
    user=CustomUser.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('adminpanel:userslist')

def adduser(request):
    
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
                return redirect('adminpanel:adduser')
            
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'email already taken!!')
                return redirect('adminpanel:adduser')
            
            else:
                user = CustomUser.objects.create_user(first_name=firstname,last_name=lastname,email=email,password=password1,phone=phone)
                user.is_superuser=True
                user.save()
                return redirect('adminpanel:userslist')
        else:
            messages.error(request, 'password do not maching!!')
            return redirect('adminpanel:adduser')
               
    return render(request,'adduser.html')

def categorylist(request):
    categories= category.objects.all()
    paginator = Paginator(categories,8)
    page= request.GET.get('page')
    paged_categories = paginator.get_page(page) 
    dict_category={
        'categories':  paged_categories 
    }
    return render(request,'category.html',dict_category)

def delete_category(request,category_id):
    catogory= category.objects.get(id=category_id)
    catogory.delete()
    return redirect('adminpanel:categorylist')


def update_category(request, category_id):
    if request.method == 'POST':
        category_instance = category.objects.get(id=category_id)
        new_category_name = request.POST['category_name']
        slug = request.POST['slug']

        # Check if the new category name already exists
        if category.objects.filter(category_name=new_category_name).exists():
            messages.error(request, 'Category already exists!!')
            return redirect('adminpanel:categorylist')

        # Update the category name and save the instance
        category_instance.category_name = new_category_name
        category_instance.slug = slug
        category_instance.save()

        return redirect('adminpanel:categorylist')
    else:
        # Get the category instance to be updated
        category_instance = category.objects.get(id=category_id)

        context = {
            'update': category_instance,
        }

        return render(request, 'updatecategory.html', context)

        
def addcategory(request,):
    
    if request.method=='POST':
        category_name = request.POST['category_name']
        slug = request.POST['slug']
        if category.objects.filter(category_name= category_name).exists():
            messages.error(request,'category already exist!!')
            return redirect('adminpanel:categorylist')
        else:
            catogory= category.objects.create(category_name=category_name, slug= slug)
            catogory.save()
            return redirect('adminpanel:categorylist')
        
    return render(request,'addcategory.html')

def subcategorylist(request):
    sub= subcategory.objects.all()
    paginator = Paginator(sub,8)
    page= request.GET.get('page')
    paged_sub = paginator.get_page(page) 
    context2={
        'sub':paged_sub
    }
    return render(request,'subcategory.html',context2)

def delete_subcategory(request,subcategory_id):
    subcatogory= subcategory.objects.get(id=subcategory_id)
    subcatogory.delete()
    return redirect('adminpanel:subcategorylist')


   
def update_subcategory(request, subcategory_id):
    subcategory_instance = subcategory.objects.get(id=subcategory_id)

    if request.method == 'POST':
        subcategory_name = request.POST['subcategory_name']
        slug = request.POST['slug']
        category_id = request.POST['category']

        # Check if the new subcategory name already exists
        if subcategory.objects.filter(subcategory_name=subcategory_name).exclude(id=subcategory_id).exists():
            messages.error(request, 'Subcategory already exists!!')
            return redirect('adminpanel:subcategorylist')
        else:
            subcategory_instance.subcategory_name = subcategory_name
            subcategory_instance.slug = slug
            subcategory_instance.category_id = category_id
            subcategory_instance.save()

            return redirect('adminpanel:subcategorylist')
        
    # Retrieve all categories for the dropdown menu
    categories= category.objects.all()
     
    # If it's a GET request, render the update form
    context3 = {
        'updatesubcategory': subcategory_instance,
        'categories': categories
    }
    
    return render(request, 'updatesubcategory.html', context3, )



def addsubcategory(request):
    
    if request.method=='POST':
        subcategory_name= request.POST['subcategory_name']
        slug = request.POST['slug']
        categoryy = request.POST['category']
        if subcategory.objects.filter(subcategory_name= subcategory_name).exists():
            messages.error(request,'subcategory already exist!!')
            return redirect('adminpanel:subcategorylist')
        else:
            subcatogory= subcategory.objects.create(subcategory_name=subcategory_name,slug=slug,category_id=categoryy)
            subcatogory.save()
            return redirect('adminpanel:subcategorylist')
        
   
    # Retrieve all categories for the dropdown menu
    
    categories= category.objects.all()
    
    return render(request, 'addsubcategory.html', {'categories': categories})

def productlist(request):
    products= product.objects.all()
    paginator = Paginator(products,4)
    page= request.GET.get('page')
    paged_products = paginator.get_page(page)

    context3={
       'products': paged_products
    }
    print(context3,'helooooo')
    
    return render(request,'product.html',context3)

def addproduct(request):

     if request.method=='POST':
        product_name= request.POST['product_name']
        slug = request.POST['slug']
        description= request.POST['description']
        price= request.POST['price']
        stock= request.POST['stock']
        image1 = request.FILES.get('image1') 
        image2= request.FILES.get('image2')
        image3= request.FILES.get('image3')
        available= request.POST['available']
        subcategoryy= request.POST['subcategory']
        categoryy = request.POST['category']
        if product.objects.filter(product_name= product_name).exists():
            messages.error(request,'product already exist!!')
            return redirect('adminpanel:productlist')
        else:
            productt= product.objects.create( product_name=product_name,slug=slug,description=description,price=price,stock=stock,image1=image1,image2=image2,image3=image3,is_available=available,sub_category_id=subcategoryy,category_id=categoryy)
            productt.save()
            return redirect('adminpanel:productlist')
     
        
   
       # Retrieve all categories for the dropdown menu
    
     categories= category.objects.all()
     subcategories= subcategory.objects.all()
     context4={
        'categories': categories,
        'subcategories':subcategories
     }
    
     return render(request,'addproduct.html',context4 )

def delete_product(request,product_id):
    productt= product.objects.get(id=product_id)
    productt.delete()
    return redirect('adminpanel:productlist')

def update_product(request,product_id):
    product_instance = product.objects.get(id=product_id)

    if request.method == 'POST':
        product_name= request.POST['product_name']
        slug = request.POST['slug']
        description= request.POST['description']
        price= request.POST['price']
        stock= request.POST['stock']
        image1 = request.FILES.get('image1')
        image2= request.FILES.get('image2')
        image3= request.FILES.get('image3') 
        available= request.POST['available']
        subcategoryy= request.POST['subcategory']
        categoryy = request.POST['category']

                # Check if the new subcategory name already exists
        if product.objects.filter(product_name=product_name).exclude(id=product_id).exists():
                messages.error(request, 'product already exists!!')
                return redirect('adminpanel:productlist')
        else:
                product_instance.product_name= product_name
                product_instance.slug= slug
                product_instance.description= description
                product_instance.price= price
                product_instance.stock= stock
                product_instance.image1= image1
                product_instance.image2= image2
                product_instance.image3= image3
                product_instance.is_available=available
                product_instance.sub_category_id=subcategoryy
                product_instance.category_id = categoryy
                product_instance.save()

                return redirect('adminpanel:productlist')
                
        # Retrieve all categories for the dropdown menu
    categories= category.objects.all()
    subcategories= subcategory.objects.all()
        
        # If it's a GET request, render the update form
    context3 = {
            'updateproduct': product_instance,
            'categories': categories,
            'subcategories':subcategories
        }
        
    return render(request, 'updateproduct.html', context3, )

def orderslist(request):
    orders= Order.objects.all()
    paginator = Paginator(orders,10)
    page= request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context={
        'orders': paged_orders
    }
    return render(request,'orderslist.html',context)


def update_order(request, id):
  if request.method == 'POST':
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')
    order.status = status 
    order.save()
    if status  == "Delivered":
      try:
          payment = Payment.objects.get(payment_id = order.order_number, status = False)
          print(payment)
          if payment.payment_method == 'Cash on Delivery':
              payment.status = True
              payment.save()
      except:
          pass
    order.save()
    
  return redirect('adminpanel:orderslist')


def adminsearch(request):
   users = None
   categories = None
   sub = None
   products = None
   orders=None
   

   if 'keyword' in request.GET:
       keyword = request.GET['keyword']
       if keyword:
           users = CustomUser.objects.order_by('-first_name').filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword))
           categories = category.objects.order_by('-category_name').filter(Q(slug__icontains=keyword)|Q(category_name__icontains=keyword))
           sub = subcategory.objects.order_by('-subcategory_name').filter(Q(slug__icontains=keyword)|Q(subcategory_name__icontains=keyword))
           products = product.objects.order_by('-created_at').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
           orders = Order.objects.order_by('-created_at').filter(Q(order_number__icontains=keyword)|Q(payment__payment_method__icontains=keyword))
          
           
           print('kooooi')
    #    else:
        #    return redirect('users')
   context = {
           'users':users,
           'categories':categories,
           'sub':sub,
           'products':products,
           'orders':orders,
           

         }       
   return render(request,'admin_search.html',context)
 






        
