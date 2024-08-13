from django.shortcuts import render, redirect
from office.models import *
from store.models import *
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from ajax.views import *
# Create your views here.
def in_home(request):
    if request.session.has_key('in_mobile'):
        in_mobile = request.session['in_mobile']
        e=In_employee.objects.filter(mobile=in_mobile,status=1).first()
        context={}
        if e:
            e=In_employee.objects.get(mobile=in_mobile)
        context={
            'e':e
        }
        return render(request, 'store/in_home.html', context)
    else:
        return redirect('login')
    
def out_home(request):
    if request.session.has_key('out_mobile'):
        out_mobile = request.session['out_mobile']
        e=Out_employee.objects.filter(mobile=out_mobile).first()
        context={}
        if e:
            pass
        context={
            'e':e
        }
        return render(request, 'store/out_home.html', context)
    else:
        return redirect('login')

@csrf_exempt
def search_in_item(request):
    if request.session.has_key('in_mobile'):
        in_mobile = request.session['in_mobile']
        e=In_employee.objects.filter(mobile=in_mobile).first()
        in_stock_list = []
        if e:
            item = Item.objects.all().order_by('-sr_num')
            if item:
                for i in item:
                    i_name = In_item.objects.filter(in_employee_id=e.id,item_id=i.id,date__gte=date.today(),date__lte=date.today()).first()
                    if i_name:
                        in_stock_list.append(i_name)
        context={
            'e':e,
            'in_stock_list':in_stock_list,
            'item':item
        }
        return render(request, 'store/search_in_item.html', context)
    else:
        return redirect('login')


def item_in(request,item_id):
    if request.session.has_key('in_mobile'):
        in_mobile = request.session['in_mobile']
        e=In_employee.objects.filter(mobile=in_mobile).first()
        context={}
        if e:
            b = Batch.objects.filter(item_id=item_id).count()
            if b == 0:
                batch_save(item_id,e.id)
                b_id = Batch.objects.filter(item_id=item_id).last()
            else:
                b_id = Batch.objects.filter(item_id=item_id).last()
        context={
            'e':e,
            'url_in':f'/store/item_in/{item_id}',
            'i':Item.objects.get(id=item_id),
            'b_id':b_id,
        }
        return render(request, 'store/item_in.html', context)
    else:
        return redirect('login')
    
def add_voucher(request):
    if request.session.has_key('out_mobile'):
        out_mobile = request.session['out_mobile']
        e=Out_employee.objects.filter(mobile=out_mobile).first()
        context={}
        if e:
            e=Out_employee.objects.get(mobile=out_mobile)
            if 'Add_voucher'in request.POST:
                voucher_name = request.POST.get('voucher_name')
                Voucher_name(
                    out_employee_id = e.id,
                    name = voucher_name,
                    verify_status = 0
                ).save()
                v = Voucher_name.objects.filter(out_employee_id=e.id).last()
                return redirect(f'/store/item_out/{v.id}')
        context={
            'e':e
        }
        return render(request, 'store/add_voucher.html', context)
    else:
        return redirect('login')
    
def item_out(request, id):
    if request.session.has_key('out_mobile'):
        out_mobile = request.session['out_mobile']
        e=Out_employee.objects.filter(mobile=out_mobile,status=1).first()
        context={}
        vi_item = []
        if e:
            e=Out_employee.objects.get(mobile=out_mobile)
            it = Item.objects.all()
            for i in it:
                vi = Out_item.objects.filter(voucher_id=id,item_id=i.id).first()
                if vi:
                    vi_item.append(vi)
        context={
            'e':e,
            'v':Voucher_name.objects.get(id=id),
            'url':f'/store/item_out/{id}',
            'vi_item':vi_item
        }
        return render(request, 'store/item_out.html', context)
    else:
        return redirect('login')

def operator_home(request):
    if request.session.has_key('operator_mobile'):
        operator_mobile = request.session['operator_mobile']
        e=Operator.objects.filter(mobile=operator_mobile,status=1).first()
        context={}
        vi_item = []
        if e:
            if 'select_helper'in request.POST:
                in_employee_id = request.POST.get('in_employee_id')
                in_employee = In_employee.objects.get(id=in_employee_id)
                in_employee.working_status = 1
                in_employee.operator_id = e.id
                in_employee.save()
                return redirect('/store/operator_home/')
            if 'De_select_helper'in request.POST:
                in_employee_id = request.POST.get('in_employee_id')
                in_employee = In_employee.objects.get(id=in_employee_id)
                in_employee.working_status = 0
                in_employee.operator_id = None
                in_employee.save()
                return redirect('/store/operator_home/')
        context={
            'e':e,
            'in_employee':In_employee.objects.filter(status=1,working_status=0),
            'in_employee_selected':In_employee.objects.filter(status=1,working_status=1,operator_id=e.id),
            'in_employee_selected_count':In_employee.objects.filter(status=1,working_status=1,operator_id=e.id).count(),
        }
        return render(request, 'store/operator/operator_home.html', context)
    else:
        return redirect('login')



































































































































































































































































































































































































