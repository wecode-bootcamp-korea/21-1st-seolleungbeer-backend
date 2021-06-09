from django.db                 import models
from django.db.models.deletion import CASCADE

class User(models.Model):
    sex           = models.CharField(max_length=50)
    name          = models.CharField(max_length=50)
    password      = models.CharField(max_length=100)
    email         = models.CharField(max_length=50, unique=True)
    mobile        = models.CharField(max_length=50, unique=True)
    profile_image = models.CharField(max_length=200, blank=True)
    like          = models.ManyToManyField('products.Product', through='Like')

    class Meta:
        db_table = 'users'                                                                                                                                                              

class Like(models.Model):
    users    = models.ForeignKey('User', on_delete=CASCADE)
    products = models.ForeignKey('products.Product', on_delete=CASCADE)

    class Meta:
        db_table = 'likes'