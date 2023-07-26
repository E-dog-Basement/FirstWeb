import json
from django.shortcuts import render, redirect, HttpResponse
from app01 import models
import random
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils.pagination import Pagination
from app01.utils.forms import OrderForm


def order_list(request):
    serach_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        serach_dict['username__contains'] = search_data

    order_set = models.Order.objects.filter(**serach_dict).order_by('-id')

    page_object = Pagination(request, data_set=order_set)
    page_set = page_object.page_set
    page_str = page_object.html()



    form = OrderForm()
    context = {
        'form': form,
        'page_set': page_set,
        'search_data': search_data,
        'page_str': page_str,
    }

    return render(request, 'order_list.html', context)

@csrf_exempt
def order_add(request):
    form = OrderForm(data=request.POST)

    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,9999))
        form.instance.admin_id = request.session['info']['id']
        form.save()

        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})


def order_delete(request, nid):
    exist = models.Order.objects.filter(id=nid).exists()
    if not exist:
        return JsonResponse({"status": False, "error":"此数据不存在"})

    models.Order.objects.filter(id=nid).delete()
    return JsonResponse({"status": True})

def order_edit(request):
    id = request.GET.get('uid')
    exist = models.Order.objects.filter(id=id).exists()
    if not exist:
        return JsonResponse({"status": False, "error":"此数据不存在"})

    context = {
        'status': True,
        'data': models.Order.objects.filter(id=id).values('title', 'price','status').first()
    }
    return JsonResponse(context)


def order_editSave(request):
    id = request.GET.get('id')
    form = OrderForm(data=request.GET, instance=models.Order.objects.filter(id=id).first())
    if form.is_valid():
        form.save()
        context = {
            'status': True
        }
        return JsonResponse(context)
    else:
        context = {
            'status': False,
            'error': '修改失败'
        }
        return JsonResponse(context)

