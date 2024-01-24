from django.urls import path
from . import views



urlpatterns = [
    path('login',views.loginn, name='loginn'),
    path('registration',views.signup, name='signup'),
    path('logout',views.logout, name='logout')
]