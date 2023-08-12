from django.http import JsonResponse
from django.shortcuts import render, redirect
from app01 import models
from django.views.decorators.csrf import csrf_exempt



# Create your views here.


def depart_list(request):
    department = models.Department.objects.all()

    return render(request, 'depart_list.html', {'department': department})


@csrf_exempt
def depart_add(request):
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    new_department = request.POST.get('depart')

    models.Department.objects.create(department_name=new_department)

    return redirect('/depart/list/')


def depart_delete(request, nid):
    exist = models.Department.objects.filter(id=nid).exists()
    if not exist:
        return JsonResponse({"status": False, "error":"此数据不存在"})

    models.Department.objects.filter(id=nid).delete()
    return JsonResponse({"status": True})


@csrf_exempt
def depart_edit(request, nid):
    if request.method == 'GET':
        depart_object = models.Department.objects.filter(id=nid).first()


        return render(request, 'depart_edit.html', {'depart_object': depart_object})

    update_department = request.POST.get('depart')
    models.Department.objects.filter(id=nid).update(department_name=update_department)

    return redirect('/depart/list/')