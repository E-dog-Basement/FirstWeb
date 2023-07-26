# Generated by Django 4.2.2 on 2023-07-24 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_admin_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=64, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=32, verbose_name='Username'),
        ),
    ]
