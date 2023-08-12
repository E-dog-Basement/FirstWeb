from django.http import JsonResponse
from django.shortcuts import render, redirect
from app01 import models
from django.views.decorators.csrf import csrf_exempt
from app01.utils.pagination import Pagination
from app01.utils.forms import UserForm


def user_list(request):
    employee_set = models.Employee.objects.all()

    page_object = Pagination(request, data_set=employee_set, page_size=10 )

    page_set = page_object.page_set
    page_str = page_object.html()
    context = {
        'employee_set': page_set,
        'page_str': page_str
    }

    return render(request, 'user_list.html', context)


@csrf_exempt
def user_add(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'user_add.html', {'form': form})

    form = UserForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'user_add.html', {'form': form})


@csrf_exempt
def user_edit(request, nid):
    row_object = models.Employee.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = UserForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:

        return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    exist = models.Employee.objects.filter(id=nid).exists()
    if not exist:
        return JsonResponse({"status": False, "error":"此数据不存在"})

    models.Employee.objects.filter(id=nid).delete()
    return JsonResponse({"status": True})