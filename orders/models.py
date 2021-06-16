from django.db                 import models
from django.db.models.deletion import CASCADE

from users.models import User

class Order(models.Model):
    order_number        = models.CharField(max_length=100, unique=True)
    created_at          = models.DateTimeField(auto_now=True)
    delivery_charge     = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    delivery_method     = models.CharField(max_length=100, null=True)
    delivery_memo       = models.CharField(max_length=100, null=True)
    payment_information = models.CharField(max_length=50, null=True)
    payment_charge      = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    user                = models.ForeignKey('users.User', on_delete=CASCADE)
    order_status        = models.ForeignKey('OrderStatus', on_delete=CASCADE)
    product             = models.ManyToManyField('products.Product', through='OrderItem')
    
    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    PENDING = 1
    PAIDED  = 2
    status  = models.CharField(max_length=50)

    class Meta:
        db_table = 'order_statuses'

class OrderItem(models.Model):
    amount  = models.IntegerField()
    product = models.ForeignKey('products.Product', on_delete=CASCADE)
    order   = models.ForeignKey('Order', on_delete=CASCADE)

    class Meta:
        db_table = 'order_items'