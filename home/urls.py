from django.urls import path
from . import views



urlpatterns = [
    path('',views.home, name='home'),
    #path('category/',views.categoryy, name='category'),
    path('category/',views.categoryy, name='category'),
    path('product/<int:product_id>/',views.productdetails,name='product'),
    
   
]