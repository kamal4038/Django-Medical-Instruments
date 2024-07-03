from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
import os
from datetime import timedelta

class Register(models.Model):
    GENDER_CHOICES=[
        ('M','Male'),
        ('F','Female'),
    ]
    username=models.CharField(max_length=100)
    userid=models.CharField(primary_key = True,max_length=100)
    password=models.CharField(max_length=100)
    dob=models.DateField()
    mobile_number=models.CharField(max_length=100)
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES)
    address=models.CharField(max_length=150)
    photo=models.ImageField()

    def __str__(self):
        return self.userid
def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")   
    new_filename="%s%s"%(now_time,filename) 
    return os.path.join('uploads/',new_filename)

class Category(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.TextField(max_length=150,null=True,blank=True)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at=models.DateTimeField(auto_now_add=True)
    
def __str__(self):
    return self.name
    



class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    vendor=models.CharField(max_length=150,null=False,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.TextField(max_length=150,null=True,blank=True)
    rent=models.CharField(max_length=150,default=0) 
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at=models.DateTimeField(auto_now_add=True)
    product_id=models.CharField(default=0,max_length=150)
    rent_rate=models.FloatField(default=0)
     
def __str__(self):
    return  self.name

class Cart(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

class Rental(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(default=0)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    start_date = models.DateField(null=False,blank=False)
    return_date = models.DateField(null=False,blank=False)
    total_days=models.CharField(max_length=150,null=False,blank=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)    


class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    order_date = models.DateField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)   






class Cart1(models.Model):
    user=models.OneToOneField(Register,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product,through='CartItem')

    def __str__(self):
        return f"Cart1 of {self.user.username}"
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart1,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class Rent1(models.Model):
     user=models.OneToOneField(Register,on_delete=models.CASCADE)
     products=models.ManyToManyField(Product,through='RentItem')

class RentItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)     
    rental=models.ForeignKey(Rent1,on_delete=models.CASCADE)
    rent_quantity=models.PositiveIntegerField(default=1)
    rent_startdate=models.DateField()
    rent_enddate=models.DateField()


    @property
    def rent_days(self):
        return (self.rent_enddate - self.rent_startdate) + 1
    
    @property
    def rent_amount(self):
        return self.rent_days * self.product.rent_rate