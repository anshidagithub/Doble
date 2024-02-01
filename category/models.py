from django.db import models
from account.models import CustomUser

# Create your models here.

class category(models.Model):
    category_name= models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null= True)
    created_at= models.DateField(auto_now=True)
    updated_at= models.DateField(auto_now=True)
    class mata:
        verbose_name= 'category'
        verbose_name_plural= 'categories'

    def __str__(self):
        return self.category_name
    
class subcategory(models.Model):
    subcategory_name= models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null= True)
    category= models.ForeignKey(category,on_delete=models.CASCADE)
    created_at= models.DateField(auto_now=True)
    updated_at= models.DateField(auto_now=True)
    class meta:
        verbose_name= 'subcategory'
        verbose_name_plural= 'subcategories'

    def __str__(self):
        return self.subcategory_name

class product(models.Model):
    product_name= models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null= True)
    description= models.CharField(max_length=200,blank=True)
    price= models.IntegerField()
    image1= models.ImageField(upload_to='photos/product')
    image2= models.ImageField(upload_to='photos/product')
    image3= models.ImageField(upload_to='photos/product')
    stock= models.IntegerField()
    is_available= models.BooleanField()
    category= models.ForeignKey(category,on_delete=models.CASCADE)
    sub_category= models.ForeignKey(subcategory,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at= models.DateField(auto_now=True)

    def __str__(self):
        return self.product_name
    

class cart(models.Model):
    cart_id= models.CharField(max_length=250,blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_added= models.DateField(auto_now=True)

    def __str__(self):
        return self.cart_id
    
class cartitem(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    product= models.ForeignKey(product,on_delete=models.CASCADE)
    cart= models.ForeignKey(cart,on_delete=models.CASCADE,null=True)
    quantity= models.IntegerField()
    is_active= models.BooleanField(default=True)

    def sub_totel(self):
        return self.product.price*self.quantity

    #def __str__(self):
        #return self.product
    
    def __unicode__(self):
        return self.product   
        
