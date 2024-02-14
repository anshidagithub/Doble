from django.shortcuts import render,redirect
from category.models import category,subcategory,product,cartitem
from django.shortcuts import render, get_object_or_404
from category.views import _cart_id
from django.db.models import Q
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.

def home(request):
     products= product.objects.all().filter(is_available=True)[:4]
     context= {
          'products': products,
     }
     return render(request,'home.html',context)

def categoryy(request,sub_category_slug=None):
    sub_category = None
    products = None
    categories = None
    
    
    if sub_category_slug !=None:
        print("hoooy")
        sub_category = get_object_or_404(subcategory,slug=sub_category_slug)
        products = product.objects.filter(sub_category=sub_category,is_available=True)
        categories = category.objects.all()
        sub = subcategory.objects.all()
        Paginattor= Paginator(products,3)
        page= request.GET.get('page')
        paged_products= Paginattor.get_page(page)
        
        
    else:
        print('koi')
        categories = category.objects.all()
        sub = subcategory.objects.all()
        products = product.objects.all()
        Paginattor= Paginator(products,6)
        page= request.GET.get('page')
        paged_products= Paginattor.get_page(page)

        
    context = {
        'categories' : categories,
        'sub':sub,
        'products':paged_products,
        
    }
    return render(request,'fcategory.html',context)

def productdetails(request,product_id):
    singleproduct= product.objects.get(id=product_id)
    in_cart= cartitem.objects.filter(cart__cart_id=_cart_id(request), product=singleproduct).exists()
    context6={
        'singleproduct':singleproduct,
        'in_cart' : in_cart
    }
    return render(request,'fproduct.html',context6)

def search(request):
   categories = category.objects.all()
   sub = subcategory.objects.all()
   products = None
   if 'keyword' in request.GET:
       keyword = request.GET['keyword']
       if keyword:
           products = product.objects.order_by('-created_at').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
           
           print('kooooi')
       else:
           return redirect('home')
   context = {
          'products':products,
          'categories':categories,
          'sub':sub

        }       
   return render(request,'fcategory.html',context)

