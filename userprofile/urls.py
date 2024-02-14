
from django.urls import path
from . import views

urlpatterns = [
   path('userdash/', views.userdash,name='userdash'),
   path('my_orders/', views.my_orders,name='my_orders'),
   path('edit_profile/', views.edit_profile,name='edit_profile'),
   path('change_password/', views.change_password,name='change_password'),
   path('order_details/<int:order_id>/', views.order_details,name='order_details'),
   path("cancel_order/<int:order_number>/",views.cancel_order,name='cancel_order'), 
   path("return_order/<int:order_number>/",views.return_order,name='return_order'), 
   path('myAddress/', views.myAddress, name='myAddress'),
   path('addAddress/', views.addAddress, name='addAddress'),
   path('editAddress/<int:id>/', views.editAddress, name='editAddress'),
   path('deleteAddress/<int:id>/', views.deleteAddress, name='deleteAddress'),
]