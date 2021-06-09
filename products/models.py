from django.db                 import models
from django.db.models.deletion import CASCADE

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    sub_name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey('Category', on_delete=CASCADE)

    class Meta:
        db_table = 'sub_categories'

class Product(models.Model):
    korean_name  = models.CharField(max_length=50, unique=True)
    english_name = models.CharField(max_length=50, unique=True)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    description  = models.CharField(max_length=100, unique=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=CASCADE)
    product_info = models.OneToOneField('ProductInfo', on_delete=CASCADE, default='')

    class Meta:
        db_table = 'products'

class ProductInfo(models.Model):
    meterial     = models.CharField(max_length=50)
    size         = models.CharField(max_length=50)
    manufaturer  = models.CharField(max_length=50)
    made         = models.CharField(max_length=50)
    distributor  = models.CharField(max_length=50)
    afterservice = models.CharField(max_length=50)

    class Meta:
        db_table = 'product_infos'

class ImageType(models.Model):
    type    = models.CharField(max_length=50, default='')
    product = models.ManyToManyField('Product', through='ProductImage')

    class Meta:
        db_table = 'image_types'

class ProductImage(models.Model):
    image_url  = models.CharField(max_length=200)
    product    = models.ForeignKey('Product', on_delete=CASCADE)
    image_type = models.ForeignKey('ImageType', on_delete=CASCADE)

    class Meta:
        db_table = 'product_images'