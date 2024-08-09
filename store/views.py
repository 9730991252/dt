from django.shortcuts import render, redirect
from office.models import *
from store.models import *
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from ajax.views import *
# Create your views here.
def store_dashboard(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Employee.objects.filter(mobile=store_mobile).first()
        context={}
        if e:
            e=Employee.objects.get(mobile=store_mobile)
        context={
            'e':e
        }
        return render(request, 'store/store_dashboard.html', context)
    else:
        return redirect('login')

@csrf_exempt
def search_in_item(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Employee.objects.filter(mobile=store_mobile).first()
        in_stock_list = []
        if e:
            item = Item.objects.all()
            if item:
                for i in item:
                    i_name = In_item.objects.filter(employee_id=e.id,item_id=i.id,date__gte=date.today(),date__lte=date.today()).first()
                    if i_name:
                        in_stock_list.append(i_name)
        context={
            'e':e,
            'in_stock_list':in_stock_list
        }
        return render(request, 'store/search_in_item.html', context)
    else:
        return redirect('login')


def item_in(request,item_id):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Employee.objects.filter(mobile=store_mobile).first()
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
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Employee.objects.filter(mobile=store_mobile).first()
        context={}
        if e:
            e=Employee.objects.get(mobile=store_mobile)
            if 'Add_voucher'in request.POST:
                voucher_name = request.POST.get('voucher_name')
                Voucher_name(
                    employee_id = e.id,
                    name = voucher_name,
                    verify_status = 0
                ).save()
                v = Voucher_name.objects.filter(employee_id=e.id).last()
                return redirect(f'/store/item_out/{v.id}')
        context={
            'e':e
        }
        return render(request, 'store/add_voucher.html', context)
    else:
        return redirect('login')
    
def item_out(request, id):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Employee.objects.filter(mobile=store_mobile).first()
        context={}
        vi_item = []
        if e:
            e=Employee.objects.get(mobile=store_mobile)
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




































































































































































































































































































































































































