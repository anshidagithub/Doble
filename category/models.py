from django.db import models

# Create your models here.

class category(models.Model):
    category_name= models.CharField(max_length=50, unique=True)
    created_at= models.DateField(auto_now=True)
    updated_at= models.DateField(auto_now=True)
    class mata:
        verbose_name= 'category'
        verbose_name_plural= 'categories'

    def __str__(self):
        return self.category_name
    
class subcategory(models.Model):
    subcategory_name= models.CharField(max_length=50)
    category= models.ForeignKey(category,on_delete=models.CASCADE)
    created_at= models.DateField(auto_now=True)
    updated_at= models.DateField(auto_now=True)
    class meta:
        verbose_name= 'subcategory'
        verbose_name_plural= 'subcategories'

    def __str__(self):
        return self.subcategory_name

class product(models.Model):
    product_name= models.CharField(max_length=100)
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
    
        
