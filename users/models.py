from django.db import models

class User(models.Model):
    sex           = models.IntegerField(null=True)
    profile_image = models.CharField(max_length=200)
    password      = models.CharField(max_length=100, null=True)
    email         = models.CharField(max_length=50, unique=True, null=True)
    mobile        = models.CharField(max_length=50, unique=True, null=True)
    name          = models.CharField(max_length=50, unique=True, null=True)

    class Meta:
        db_table = 'users'