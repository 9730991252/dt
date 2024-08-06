from django.shortcuts import render, redirect
from office.models import *
from store.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import timedelta, date
from django.core.paginator import Paginator
# Create your views here.
def office_dashboard(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        context={}
        ti_item = []
        all_stock_list = []
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
            i=Item.objects.all()
            for i in i:
                ti = In_item.objects.filter(item_id=i.id,date__gte=date.today(),date__lte=date.today()).order_by('-id').first()
                if ti:
                    ti_item.append(ti)
                ########################
                print(i.id)
                s = In_item.objects.filter(item_id=i.id,status=1).first()
                if s:
                    all_stock_list.append(s)
        context={
            'e':e,
            't':ti_item,
            'all_stock_list':all_stock_list,
        }
        return render(request, 'office/office_dashboard.html', context)
    else:
        return redirect('login')
    

def employee(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
        context={}

        if 'add_employee'in request.POST:
            name=request.POST.get('name')
            mobile=request.POST.get('mobile')
            pin=request.POST.get('pin')
            department=request.POST.get('department')
            if Employee.objects.filter(mobile=mobile).exists():
                messages.success(request,"Employee Allready Exits")
            else:
                Employee(
                    name=name,
                    mobile=mobile,
                    pin=pin,
                    department=department,
                    ).save()
                messages.success(request,"Employee Add Succesfully") 
        elif "Active" in request.POST:
            id=request.POST.get('id')
            #print(id)
            ac=Employee.objects.get(id=id)
            ac.status='0'
            ac.save()
        elif "Deactive" in request.POST:
            id=request.POST.get('id')
            #print(id)
            ac=Employee.objects.get(id=id)
            ac.status='1'
            ac.save() 

        elif "Edit" in request.POST:
            id=request.POST.get('id')
            name=request.POST.get('name')
            print(name)
            mobile=request.POST.get('mobile')
            pin=request.POST.get('pin')
            department=request.POST.get('department')
            #print(id)
            Employee(
                id=id,
                name=name,
                mobile=mobile,
                pin=pin,
                department=department,
            ).save()
            messages.success(request,"Employee Edit Succesfully") 

        context={
            'e':e,
            'em':Employee.objects.all()
        }
        return render(request, 'office/employee.html', context)
    else:
        return redirect('login')
    



def item(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
        context={}

        if 'add_item'in request.POST:
            name=request.POST.get('name')
            Item(
                name=name,
                employee_id=e.id
                ).save()
            messages.success(request,"Item Add Succesfully")
            return redirect('item')
        elif "Active" in request.POST:
            id=request.POST.get('id')
            #print(id)
            ac=Item.objects.get(id=id)
            ac.status='0'
            ac.save()
            return redirect('item')
        elif "Deactive" in request.POST:
            id=request.POST.get('id')
            #print(id)
            ac=Item.objects.get(id=id)
            ac.status='1'
            ac.save() 
            return redirect('item')

        elif "Edit" in request.POST:
            id=request.POST.get('id')
            name=request.POST.get('name')
            #print(id)
            Item(
                id=id,
                name=name,
                employee_id=e.id
            ).save()
            messages.success(request,"Item Edit Succesfully") 
            return redirect('item')

        context={
            'e':e,
            'p':Item.objects.all()
        }
        return render(request, 'office/item.html', context)
    else:
        return redirect('login')


@csrf_exempt  
def batch_number(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile'] 
        p = ''
        b = ''
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
            if 'Select_Item' in request.POST:
                pid=request.POST.get('p_id')
                p=Item.objects.get(id=pid)
                b = Batch.objects.filter(item_id=pid)
        context={
            'e':e,
            'p':p,
            'b':b
        }
        return render(request,'office/batch_number.html',context=context)        
    else:
        return redirect('login')



@csrf_exempt
def generate_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        p='' 
        b='' 
        ba='' 
        pr='' 
        qr='' 
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
        if 'Select_Item' in request.POST:
            pid=request.POST.get('p_id')
            b = Batch.objects.filter(item_id=pid).order_by('-id')
            p=Item.objects.get(id=pid)
        if 'Select_Batch' in request.POST:
            bid = request.POST.get('bid')
            ba = Batch.objects.get(id=bid)
            pr = Item.objects.get(id=ba.item_id)
            qr = Qr_code.objects.filter(batch_id=bid).order_by('-id')
        context={
            'e':e,
            'p':p,
            'b':b,
            'pr':pr,
            'ba':ba,
            'qr':qr
        }
        return render(request,'office/generate_qr_code.html',context=context)        
    else:
        return redirect('login')
    







def verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
        context={
            'e':e,
        }
        return render(request,'office/verify_qr_code.html',context=context)        
    else:
        return redirect('login')


def pending_verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
        context={
            'e':e,
            'v':Voucher_name.objects.filter(verify_status=0)
        }
        return render(request,'office/pending_verify_qr_code.html',context=context)        
    else:
        return redirect('login')


 

def pending_view_voucher(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
            v = Voucher_name.objects.get(id=id)
            q = Out_item.objects.filter(voucher_id=id)
            a = Out_item.objects.filter(voucher_id=id,verify_status=1).count()
            b = Out_item.objects.filter(voucher_id=id).count()
             
        if 'Verify' in request.POST:
            qid = request.POST.get('qid')
            q = Out_item.objects.get(id=qid)
            if q.verify_status == 0:
                q.verify_status = 1
                q.verify_by = e.name
                q.verify_date = datetime.datetime.now()
                q.save()
                return redirect(f'/office/pending_view_voucher/{id}')
        if 'Voucher_Verify' in request.POST:
            v = Voucher_name.objects.get(id=id)
            v.verify_by = e.name
            v.verify_status = 1
            v.verify_date = date.today()
            v.save()
            return redirect('/office/pending_verify_qr_code')
        
        if 'Update_v' in request.POST:
            new_name_v = request.POST.get('new_name_v')
            vn = Voucher_name.objects.get(id=id)
            vn.name = new_name_v
            vn.save()
            return redirect(f'/office/pending_view_voucher/{id}')
        context={
            'e':e,
            'q':q,
            'a':a,
            'b':b,
            'v':v
        }
        return render(request,'office/pending_view_voucher.html',context=context)        
    else:
        return redirect('login')
    


    

def accepted_verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
        v = Voucher_name.objects.filter(verify_status=1)
        paginator = Paginator(v,10) 
        page_number = request.GET.get('page')
        v = paginator.get_page(page_number)
        total_pages = v.paginator.num_pages
        context={
            'e':e,
            'v': v,
            'last_page':total_pages,
            'total_page_list':[n+1 for n in range(total_pages)][0:3]
        }
        return render(request,'office/accepted_verify_qr_code.html',context=context)        
    else:
        return redirect('login')
    



    
def accepted_view_voucher(request,id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            e=Employee.objects.get(mobile=office_mobile)
            v = Voucher_name.objects.get(id=id)
            q = Out_item.objects.filter(voucher_id=id)
        context={
            'e':e,
            'v':v,
            'q':q

        }
        return render(request,'office/accepted_view_voucher.html',context=context)        
    else:
        return redirect('login')


    
 

def old_stock(request):
    if request.session.has_key('crenta_admin_mobile'):
        context={}
        t=''
        d=''
        if 'Days'in request.POST:
            day = request.POST.get('day')
            if day == '0':
                pass
            else:
                d = (date.today() - timedelta(days=int(day)))
                t = In_item.objects.filter(status=1,date__lte=d).order_by('item_id')[0:300]
            context={
                't':t,
                'd':d,
                'day':day,
            }
        return render(request,'office/old_stock.html',context)
    else:
        return render(request,'login.html')




