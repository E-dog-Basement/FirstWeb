import requests
from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django.views.decorators.csrf import csrf_exempt
from app01.utils.forms import AdminLoginForm, AdminSignUpForm, AdminForgetForm ,AdminResetForm
from io import BytesIO
from app01.utils.vertification import check_code
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import JsonResponse


def account_logout(request):
    request.session.clear()
    return redirect('/login/')


def image(request):
    image, code_string = check_code()
    request.session['image_code'] = code_string
    request.session.set_expiry(60)

    stream = BytesIO()
    image.save(stream, 'png')
    return HttpResponse(stream.getvalue())


@csrf_exempt
def account_login(request):
    if request.method == 'GET':
        form = AdminLoginForm()
        return render(request, 'login.html', {'form': form})

    # method == POST :
    form = AdminLoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        image_code = request.session.get('image_code', '')
        if user_input_code.upper() != image_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            # 登录失败
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})

        request.session['info'] = {'id': admin_object.id, 'username': admin_object.username,
                                   'logo': admin_object.logo.name}
        request.session.set_expiry(60 * 60 * 24)
        return redirect('/depart/list/')

    return render(request, 'login.html', {'form': form})


def account_RegisterEmail(request):
    receiver_email = request.GET.get('email')
    code = random.randint(100000, 999999)
    # 发邮件(同步发送 延迟会阻塞)
    subject = 'Verification Code'
    message = 'This is your Verification Code:' + str(code)
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [receiver_email]  # 收件人列表
    # html_message = 'Hello'
    send_mail(subject, message, sender, receiver, fail_silently=False)
    request.session['info'] = {'code': code}
    print(request.session['info']['code'])
    context = {
        'status': True
    }
    return JsonResponse(context)


@csrf_exempt
def sign_up(request):
    if request.method == 'GET':
        form = AdminSignUpForm()
        context = {
            'form': form,
        }
        return render(request, 'sign_in.html', context)

    form = AdminSignUpForm(data=request.POST)
    print(request.session['info']['code'])
    if form.is_valid() and request.session['info']['code'] == int(form.data['code']):
        form.save()
        return redirect('/login/')
    context = {
        'form': form,
    }
    if request.session['info']['code'] != form.data['code']:
        form.add_error('code', 'Verification Code Wrong')
    return render(request, 'sign_in.html', context)


@csrf_exempt
def reset_password(request):
    if request.method == 'GET':
        form = AdminForgetForm()
        context = {
            'form': form
        }
        return render(request, 'reset_password.html', context)

    if request.method == 'POST':
        form = AdminForgetForm(data=request.POST)
        email = form.data.get('email')
        context = {
            'form': form
        }
        try:
            if request.session['info']['code'] != int(form.data['code']):
                form.add_error('code', 'Verification code is wrong')
                return render(request, 'reset_password.html', context)
        except:
            form.add_error('code', 'Please get the verification code again')
            return render(request, 'reset_password.html', context)

        exist = models.Admin.objects.filter(email=email).exists()

        if not exist:
            form.add_error('email', 'This email is not exist')
            return render(request, 'reset_password.html', context)
        else:
            # request.session['info']['email'] = email
            request.session['info'] = {'email': email}
            print(request.session['info']['email'])
            return redirect('/account/forgetPassword/')

@csrf_exempt
def reset_password_confirm(request):
    if request.method == 'GET':
        print(request.session['info'])
        form = AdminResetForm()
        context = {
            'form': form
        }
        return render(request, 'reset_password_confirm.html', context)

    if request.method == 'POST':
        print(request.session['info'])
        email = request.session['info']['email']
        row_object = models.Admin.objects.filter(email=email).first()
        form = AdminResetForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            context = {
                'form': form
            }
            return render(request, 'reset_password_confirm.html', context)





