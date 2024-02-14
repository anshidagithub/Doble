from django.urls import path
from . import views



urlpatterns = [
    path('',views.home, name='home'),
    path('category/',views.categoryy, name='category'),
    path('sub_category/<slug:sub_category_slug>/', views.categoryy,name='product_by_sub_category'),
    path('product/<int:product_id>/',views.productdetails,name='product'),
    path('dashbord/search/', views.search,name='search'),
    
   
]