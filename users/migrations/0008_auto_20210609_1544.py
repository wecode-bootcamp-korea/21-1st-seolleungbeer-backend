# Generated by Django 3.2.4 on 2021-06-09 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210609_1544'),
        ('users', '0007_auto_20210608_1940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='products',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='users',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='product_like',
        ),
        migrations.RemoveField(
            model_name='user',
            name='product_order_item',
        ),
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(related_name='likes', through='users.Like', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(max_length=50),
        ),
    ]
