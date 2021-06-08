from django.db                 import models
from django.db.models.deletion import CASCADE

class Order(models.Model):
    order_number        = models.CharField(max_length=100, unique=True)
    delivery_method     = models.CharField(max_length=100)
    delivery_memo       = models.CharField(max_length=100, null=True)
    payment_information = models.CharField(max_length=50)
    payment_charge      = models.CharField(max_length=50)
    delivery_charge     = models.IntegerField()
    created_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)
    order  = models.ForeignKey('Order', on_delete=CASCADE)

    class Meta:
        db_table = 'order_statuses'

class OrderItem(models.Model):
    amount  = models.IntegerField()
    user    = models.ForeignKey('users.User', on_delete=CASCADE)
    product = models.ForeignKey('products.Product', on_delete=CASCADE)
    order   = models.ForeignKey('Order', on_delete=CASCADE)

    class Meta:
        db_table = 'order_items'