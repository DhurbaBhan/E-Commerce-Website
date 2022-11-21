from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


STATE_CHOICES=(
    ('Province 1','Province 1'),
    ('Madhesh Pradesh','Madhesh Pradesh'),
    ('Bagmati Pradesh','Bagmati Pradesh'),
    ('Gandaki Pradesh','Gandaki Pradesh'),
    ('Lumbini Pradesh','Lumbini Pradesh'),
    ('Karnali Pradesh','Karnali Pradesh'),
    ('Sudur Paschim Pradesh','Sudur Paschim Pradesh'),
)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_constraint=False)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.PositiveIntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)
   
    def __str__(self):
        return self.name

CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return self.title

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_constraint=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,db_constraint=False)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id) 

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price           

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)  
class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_constraint=False)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,db_constraint=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price           
    