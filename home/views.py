from django.shortcuts import render,redirect
from category.models import category,subcategory,product

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
    