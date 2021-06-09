# Generated by Django 3.2.4 on 2021-06-09 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('profile_image', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_image',
        ),
    ]