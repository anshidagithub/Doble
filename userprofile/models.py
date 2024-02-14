from django.db import models
from account.models import CustomUser

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True,max_length=100,null=True)
    address_line_2 = models.CharField(blank=True,max_length=100,null=True)
    profile_picture = models.ImageField(blank=True,upload_to='userprofile',null=True)
    city = models.CharField(blank=True,max_length=20,null=True)
    state = models.CharField(blank=True,max_length=20,null=True)
    country = models.CharField(blank=True,max_length=20,null=True)
    wallet = models.FloatField(blank=True,null=True,default=0)
    

    def __str__(self):
        return self.user.first_name
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'
    


class Address(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50,null=True)
    state =   models.CharField(max_length=50)
    country =   models.CharField(max_length=50,blank=True)
    city =   models.CharField(max_length=50,blank=True)
    order_note = models.CharField(max_length=100, blank=True)
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def address(self):
        return f"{self.address_line1} {self.address_line2}"

    def __str__(self):
        return self.first_name  