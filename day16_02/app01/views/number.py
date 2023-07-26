from django.shortcuts import render, redirect
from app01 import models
from django.views.decorators.csrf import csrf_exempt
from app01.utils.pagination import Pagination
from app01.utils.forms import NumberForm, NumberEditForm

def number_list(request):
    serach_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        serach_dict['phone_number__contains'] = search_data

    number_set = models.PhoneNumber.objects.filter(**serach_dict).order_by('-level')

    page_object = Pagination(request, data_set=number_set)

    page_set = page_object.page_set
    page_str = page_object.html()
    context = {
        'page_set': page_set,
        'search_data': search_data,
        'page_str': page_str
    }
    return render(request, 'number_list.html', context)


@csrf_exempt
def number_add(request):
    if request.method == 'GET':
        form = NumberForm()
        return render(request, 'number_add.html', {'form': form})
    form = NumberForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/number/list/')
    else:
        return render(request, 'number_add.html', {'form': form})


@csrf_exempt
def number_edit(request, nid):
    number_object = models.PhoneNumber.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = NumberEditForm(instance=number_object)
        return render(request, 'number_edit.html', {'form': form})

    form = NumberEditForm(data=request.POST, instance=number_object)
    if form.is_valid():
        form.save()
        return redirect('/number/list/')
    else:
        # form = NumberForm(data=request.POST)
        return render(request, 'number_edit.html', {'form': form})


def number_delete(request, nid):
    models.PhoneNumber.objects.filter(id=nid).delete()
    return redirect('/number/list/')
