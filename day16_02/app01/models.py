from django.db import models


# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=32)

    def  __str__(self):
        return self.department_name


class Employee(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    password = models.CharField(max_length=32)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creat_time = models.DateField(null=True)

    depart = models.ForeignKey(to='Department', on_delete=models.CASCADE, to_field='id')

    gender_choice = (
        (1, 'Man'),
        (2, 'Women')
    )
    gender = models.SmallIntegerField(choices=gender_choice)


class PhoneNumber(models.Model):
    # ID, PhoneNumber, Price, Level, Status

    phone_number = models.CharField(max_length=11)
    price = models.IntegerField()
    level_choice = (
        (1, 'Top'),
        (2, 'Middle'),
        (3, 'Low')
    )
    level = models.SmallIntegerField(choices=level_choice, default=1)

    status_level = (
        (1, 'Occupied'),
        (2, 'Free')
    )
    status = models.SmallIntegerField(choices=status_level, default=2)


class Admin(models.Model):

    email = models.EmailField(verbose_name='Email')
    username = models.CharField(max_length=32, verbose_name='Username')
    password = models.CharField(max_length=64, verbose_name='Password')
    logo = models.ImageField(upload_to='user/', default='user/default_logo.jpg')

    def  __str__(self):
        return self.username


class Order(models.Model):
    oid = models.CharField(verbose_name='订单号', max_length=64)
    title = models.CharField(verbose_name='名称', max_length=32)
    price = models.IntegerField(verbose_name='价格')

    status_choice = (
        (1, '待支付'),
        (2, '已支付')
    )

    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice, default=1)
    admin = models.ForeignKey(verbose_name='管理员', to='Admin', on_delete=models.CASCADE)


class Logo(models.Model):
    logo = models.ImageField(upload_to='city/')
    name = models.CharField(max_length=32)


