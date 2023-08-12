from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django.views.decorators.csrf import csrf_exempt
from app01.utils.pagination import Pagination
from app01.utils.forms import AdminForm, AdminEditForm, AdminResetForm, AdminLogoForm



def admin_list(request):
    serach_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        serach_dict['username__contains'] = search_data

    admin_set = models.Admin.objects.filter(**serach_dict)

    page_object = Pagination(request, data_set=admin_set)

    page_set = page_object.page_set
    page_str = page_object.html()
    context = {
        'page_set': page_set,
        'search_data': search_data,
        'page_str': page_str
    }
    return render(request, 'admin_list.html', context)

@csrf_exempt
def admin_add(request):
    title = '添加新管理员'
    if request.method == 'GET':
        form = AdminForm()
        context = {
            'title': title,
            'form': form,
        }
        return render(request, 'Add_layout.html', context)

    form = AdminForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    context = {
        'title': title,
        'form': form,
    }

    return render(request, 'Add_layout.html', context)

@csrf_exempt
def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '该数据不存在'})

    if request.method == 'GET':
        form = AdminEditForm(instance=row_object)
        context = {
            'form': form,
            'title': '编辑管理员'
        }
        return render(request, 'Add_layout.html', context)

    form = AdminEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    else:
        context = {
            'form': form,
            'title': '编辑管理员'
        }
        return render(request, 'Add_layout.html', context)


def admin_delete(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': 'The data does not exist'})
    return render(request, 'admin_delete.html')


def admin_delete_confirm(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': 'The data does not exist'})

    models.Admin.objects.filter(id=nid).delete()
    request.session.clear()
    return redirect('/login')

@csrf_exempt
def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': 'The data does not exist'})

    if request.method == 'GET':
        form = AdminResetForm()
        context = {
            'title': 'Reset Password',
            'form': form
        }
        return render(request, 'Add_layout.html', context)

    form = AdminResetForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    else:
        context = {
            'form': form,
            'title': 'Reset Password'
        }
        return render(request, 'Add_layout.html', context)

@csrf_exempt
def admin_logo(request):
    id = request.session['info'].get('id')
    admin_object = models.Admin.objects.filter(id=id).first()

    if request.method == 'GET':
        form = AdminLogoForm(instance=admin_object)
        context = {
            'form': form,
            'title': "Change Logo",
        }

        return render(request, 'Add_layout.html', context)

    form = AdminLogoForm(data=request.POST, files=request.FILES, instance=admin_object)
    if form.is_valid():

        # 删除原图片

        form.save()
        request.session['info']['logo'] = admin_object.logo.name
        request.session.set_expiry(60 * 60 * 24)
        return redirect('/admin/list')
    else:
        context = {
            'form': form,
            'title': 'Change Logo'
        }
        return render(request, 'Add_layout.html', context)

