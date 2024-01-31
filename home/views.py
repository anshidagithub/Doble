from django.shortcuts import render,redirect
from category.models import category,subcategory,product,cartitem
from django.shortcuts import render, get_object_or_404
from category.views import _cart_id

# Create your views here.

def home(request):
     return render(request,'home.html')




def categoryy(request):
     
     context5={
         'categoriess': category.objects.all(),
         'sub':subcategory.objects.all(),
         'products':product.objects.all(),
         

     }
     return render(request,'fcategory.html',context5)

def productdetails(request,product_id):
    singleproduct= product.objects.get(id=product_id)
    in_cart= cartitem.objects.filter(cart__cart_id=_cart_id(request), product=singleproduct).exists()
    context6={
        'singleproduct':singleproduct,
        'in_cart' : in_cart
    }
    return render(request,'fproduct.html',context6)

