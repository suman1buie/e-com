from django.db import models
from django.contrib.auth.models import User


class Castomer(models.Model):
    User = models.OneToOneField(to=User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=40,null=True)
    email = models.CharField(max_length=50)
  
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
    

class Order(models.Model):
    coustomer = models.ForeignKey(Castomer , on_delete=models.SET_NULL, null=True , blank=True)
    date_ordered  = models.DateTimeField(auto_now_add=True)
    competed = models.BooleanField(default=False)
    transation_id = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderItem = self.orderitem_set.all()
        for it in orderItem:
            if it.Product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

  
    

class OrderItem(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)  
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)  
    
    @property
    def get_total(self):
        total = self.Product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    castomer = models.ForeignKey(Castomer, on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)  
    address = models.CharField(max_length=150,null=False) 
    city = models.CharField(max_length=50,null=False) 
    state = models.CharField(max_length=100,null=False) 
    zipcode = models.CharField(max_length=100,null=False) 
    date_added = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return self.address
 
 
    