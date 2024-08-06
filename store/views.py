from django.shortcuts import render, redirect
from office.models import *
from store.models import *
from datetime import date

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
     
def item_in(request):
    if request.session.has_key('store_mobile'):
        store_mobile = request.session['store_mobile']
        e=Employee.objects.filter(mobile=store_mobile).first()
        context={}
        ti_item=[]
        if e:
            e=Employee.objects.get(mobile=store_mobile)
            i=Item.objects.all()
            for i in i:
                i_all_id = i.id
                ti = In_item.objects.filter(item_id=i_all_id,date__gte=date.today(),date__lte=date.today()).order_by('-id').first()
                if ti:
                    ti_item.append(ti)
        context={
            'e':e,
            'ti':ti_item,
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
        print(vi_item)
        context={
            'e':e,
            'v':Voucher_name.objects.get(id=id),
            'url':f'/store/item_out/{id}',
            'vi_item':vi_item
        }
        return render(request, 'store/item_out.html', context)
    else:
        return redirect('login')




































































































































































































































































































































































































