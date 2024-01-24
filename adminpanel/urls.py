from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'adminpanel'



urlpatterns = [
    path('dashbord/',views.dashbord, name='dashbord'),
    path('users/',views.userslist, name='userslist'),
    path('users/toggle_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('users/adduser/',views.adduser,name='adduser'),
    path('category/',views.categorylist, name='categorylist'),
    path('category/delete_category/<int:category_id>/',views.delete_category, name='delete_category'),
    path('category/update_category/<int:category_id>/',views.update_category,name='update_category'),
    path('category/addcategory/',views.addcategory,name='addcategory'),
    path('subcategory/',views.subcategorylist,name='subcategorylist'),
    path('subcategory/delete_subcategory/<int:subcategory_id>/',views.delete_subcategory, name='delete_subcategory'),
    path('subcategory/update_subcategory/<int:subcategory_id>/',views.update_subcategory, name='update_subcategory'),
    path('subcategory/addsubcategory/',views.addsubcategory,name='add_subcategory'),
    path('product/',views.productlist,name='productlist'),
    path('product/addproduct/',views.addproduct,name='add_product'),
    path('product/delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    path('product/update_product/<int:product_id>/',views.update_product,name='update_product'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)