# Generated by Django 3.2.4 on 2021-06-14 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210614_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_charge',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_charge',
            field=models.CharField(max_length=50, null=True),
        ),
    ]