from django.db import models
from account.models import CustomUser
from category.models import product

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100,blank=True,default='empty')
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField(default=0)
    status = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    


class Order(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100,blank=True)
    order_total = models.FloatField()
    order_discount = models.FloatField(default=0)
    tax = models.FloatField()
    status = models.CharField(max_length=50,choices=STATUS,default='Order Confirmed')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    return_reason = models.CharField(max_length=50, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name 
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='user_order_page')
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    def sub_total(self):
        return self.product.price * self.quantity
