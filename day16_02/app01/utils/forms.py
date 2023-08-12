from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from django.forms.widgets import NumberInput
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils import encrypt
from django.contrib.auth.forms import PasswordResetForm


class UserForm(BootStrapModelForm):
    creat_time = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = models.Employee
        fields = ['name', 'password', 'age', 'salary', 'creat_time', 'gender', 'depart']


class NumberForm(BootStrapModelForm):
    phone_number = forms.CharField(
        validators=[RegexValidator(r'^1[3-9]\d{9}$', 'Wrong Format; Please input again')]
    )

    class Meta:
        model = models.PhoneNumber
        fields = ['phone_number', 'price', 'level', 'status']

    def clean_phone_number(self):
        txt_number = self.cleaned_data['phone_number']
        exists = models.PhoneNumber.objects.filter(phone_number=txt_number).exists()
        if exists:
            raise ValidationError('This Phone Number is Exist')
        else:
            return txt_number


class NumberEditForm(BootStrapModelForm):
    phone_number = forms.CharField(
        validators=[RegexValidator(r'^1[3-9]\d{9}$', 'Wrong Format; Please input again')]
    )

    class Meta:
        model = models.PhoneNumber
        fields = ['phone_number', 'price', 'level', 'status']

    def clean_phone_number(self):
        txt_number = self.cleaned_data['phone_number']
        exists = models.PhoneNumber.objects.exclude(id=self.instance.pk).filter(phone_number=txt_number).exists()
        if exists:
            raise ValidationError('This Phone Number is Exist')
        else:
            return txt_number


class AdminForm(BootStrapModelForm):
    check_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'check_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = encrypt.md5(self.cleaned_data.get('password'))
        return pwd

    def clean_check_password(self):
        check_password = encrypt.md5(self.cleaned_data.get('check_password'))
        password = self.cleaned_data.get('password')

        if check_password != password:
            raise ValidationError('密码不一致')
        return check_password


class AdminEditForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetForm(BootStrapModelForm):
    check_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'check_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True, attrs={'placeholder': 'Password'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        exits = models.Admin.objects.filter(id=self.instance.pk, password=encrypt.md5(password)).exists()
        if exits:
            raise ValidationError('Password cannot be the same as before')
        pwd = encrypt.md5(self.cleaned_data.get('password'))
        return pwd

    def clean_check_password(self):
        check_password = encrypt.md5(self.cleaned_data.get('check_password'))
        password = self.cleaned_data.get('password')

        if check_password != password:
            raise ValidationError('Password inconsistency')
        return check_password


class AdminLoginForm(BootStrapModelForm):
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'placeholder': 'Verification Code'}),
        required=True
    )

    class Meta:
        model = models.Admin
        fields = ['email', 'password', 'code']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

    def clean_password(self):
        pwd = encrypt.md5(self.cleaned_data.get('password'))
        return pwd


class OrderForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        exclude = ['oid', 'admin']


class AdminLogoForm(BootStrapModelForm):
    exclude_field = ['logo']

    class Meta:
        model = models.Admin
        fields = ['logo']


class AdminSignUpForm(BootStrapModelForm):
    code = forms.CharField(
        label='Verification Code',
        widget=forms.TextInput(attrs={'placeholder': 'Verification Code'}),
        required=True,
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = models.Admin
        fields = ['email', 'username', 'password', 'confirm_password', 'code']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

    def clean_email(self):
        sign_email = self.cleaned_data.get('email')
        exits = models.Admin.objects.filter(email=sign_email).exists()
        if exits:
            raise ValidationError('This email has been occupied')
        return sign_email

    def clean_password(self):
        pwd = encrypt.md5(self.cleaned_data.get('password'))
        return pwd

    def clean_confirm_password(self):
        check_password = encrypt.md5(self.cleaned_data.get('confirm_password'))
        password = self.cleaned_data.get('password')

        if check_password != password:
            raise ValidationError('Password inconsistency')
        return check_password


class AdminForgetForm(BootStrapModelForm):
    code = forms.CharField(
        label='Verification Code',
        widget=forms.TextInput(attrs={'placeholder': 'Verification Code'}),
        required=True,
    )

    class Meta:
        model = models.Admin
        fields = ['email', 'code']

