from django.db import models

class User(models.Model):
    sex           = models.IntegerField()
    name          = models.CharField(max_length=50)
    password      = models.CharField(max_length=100)
    email         = models.CharField(max_length=50, unique=True)
    mobile        = models.CharField(max_length=50, unique=True)
    profile_image = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'users'