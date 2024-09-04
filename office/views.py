from django.shortcuts import render, redirect
from office.models import *
from store.models import *
from sunil.models import *
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
            i=Item.objects.all().order_by('sr_num')
            for i in i:
                ti = Select_operator_item.objects.filter(item_id=i.id,).order_by('-id').first()
                if ti:
                    ti_item.append(ti)
                ########################
                s = In_item.objects.filter(item_id=i.id,status=1).first()
                if s:
                    all_stock_list.append(s)
        context={
            'e':e,
            't':ti_item,
            'all_stock_list':all_stock_list,
            'shift':Shift.objects.filter(working_status=1),
        }
        return render(request, 'office/office_dashboard.html', context)
    else:
        return redirect('login')
    

def employee(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            context={}

            if 'add_employee'in request.POST:
                name=request.POST.get('name')
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                department=request.POST.get('department')
                if department == 'office':
                    if Employee.objects.filter(mobile=mobile).exists():
                        messages.warning(request,"Employee Allready Exits")
                    else:
                        Employee(
                            name=name,
                            mobile=mobile,
                            pin=pin,
                            ).save()
                        messages.success(request,"Employee Add Succesfully") 
                        return redirect('/office/employee/')
                if department == 'in':
                    if In_employee.objects.filter(mobile=mobile).exists():
                        messages.warning(request,"Employee Allready Exits")
                    else:
                        In_employee(
                            name=name,
                            mobile=mobile,
                            pin=pin,
                            ).save()
                        messages.success(request,"Employee Add Succesfully") 
                        return redirect('/office/employee/')
                if department == 'out':
                    if Out_employee.objects.filter(mobile=mobile).exists():
                        messages.warning(request,"Employee Allready Exits")
                    else:
                        Out_employee(
                            name=name,
                            mobile=mobile,
                            pin=pin
                            ).save()
                        messages.success(request,"Employee Add Succesfully") 
                        return redirect('/office/employee/')
            elif "Add_machine" in request.POST:
                name=request.POST.get('name')
                if name:
                    Machine(
                      name=name 
                    ).save()
                    messages.success(request,"Machine Add Succesfully") 
                    return redirect('/office/employee/')
            elif "Edit_machine" in request.POST:
                name=request.POST.get('name')
                m_id=request.POST.get('m_id')
                if name:
                    c=Machine.objects.get(id=m_id)
                    c.name=name
                    c.save()
                    messages.success(request,"Machine Edit Succesfully") 
                    return redirect('/office/employee/')
            elif "machine_Active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Machine.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "machine_Deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Machine.objects.get(id=id)
                ac.status='1'
                ac.save() 
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
            elif "In_active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=In_employee.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "In_deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=In_employee.objects.get(id=id)
                ac.status='1'
                ac.save() 
            elif "Out_active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Out_employee.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Out_deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Out_employee.objects.get(id=id)
                ac.status='1'
                ac.save() 

            elif "Edit" in request.POST:
                id=request.POST.get('id')
                name=request.POST.get('name')
                print(name)
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                #print(id)
                Employee(
                    id=id,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                ).save()
                messages.success(request,"Employee Edit Succesfully") 
                return redirect('/office/employee/')

            elif "In_Edit" in request.POST:
                id=request.POST.get('id')
                name=request.POST.get('name')
                print(name)
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                #print(id)
                In_employee(
                    id=id,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                ).save()
                messages.success(request,"Employee Edit Succesfully") 
                return redirect('/office/employee/')

            elif "Out_Edit" in request.POST:
                id=request.POST.get('id')
                name=request.POST.get('name')
                print(name)
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                #print(id)
                Out_employee(
                    id=id,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                ).save()
                messages.success(request,"Employee Edit Succesfully") 
                return redirect('/office/employee/')
            
            elif "Add_operator" in request.POST:
                name=request.POST.get('name')
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                machine_id=request.POST.get('machine_id')
                helper_limit=request.POST.get('helper_limit')
                if Operator.objects.filter(mobile=mobile).exists():
                    messages.warning(request,"Operator Allready Exits")
                else:
                    Operator(
                      name=name,
                      mobile=mobile,
                      pin=pin,
                      machine_id=machine_id,
                      helper_limit=helper_limit,
                    ).save()
                    messages.success(request,"Operator Add Succesfully") 
                    return redirect('/office/employee/')
            elif "operator_Active" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Operator.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "operator_Deactive" in request.POST:
                id=request.POST.get('id')
                #print(id)
                ac=Operator.objects.get(id=id)
                ac.status='1'
                ac.save() 
            elif "operator_Edit" in request.POST:
                o_id=request.POST.get('o_id')
                name=request.POST.get('name')
                mobile=request.POST.get('mobile')
                pin=request.POST.get('pin')
                machine_id=request.POST.get('machine_id')
                helper_limit=request.POST.get('helper_limit')
                #print(id)
                Operator(
                    id=o_id,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                    machine_id=machine_id,
                    helper_limit=helper_limit,
                ).save()
                messages.success(request,"Operator Edit Succesfully") 
                return redirect('/office/employee/')


        context={
            'e':e,
            'em':Employee.objects.all(),
            'In_employee':In_employee.objects.all(),
            'Out_employee':Out_employee.objects.all(),
            'machine':Machine.objects.all(),
            'operator':Operator.objects.all(),

        }
        return render(request, 'office/employee.html', context)
    else:
        return redirect('login')
    



def item(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={}

        if 'add_item'in request.POST:
            name=request.POST.get('name').upper()
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
            name=request.POST.get('name').upper()
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
            'p':Item.objects.all().order_by('-sr_num')
        }
        return render(request, 'office/item.html', context)
    else:
        return redirect('login')


@csrf_exempt
def generate_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            tag_list = Qr_code.objects.filter().order_by('-id')
            paginator = Paginator(tag_list,1000) 
            page_number = request.GET.get('page')
            tag_list = paginator.get_page(page_number)
            total_pages = tag_list.paginator.num_pages
        context={
            'e':e,
            'tag_list':tag_list,
            'last_page':total_pages,
            'total_page_list':[n+1 for n in range(total_pages)][0:3]
        }
        return render(request,'office/generate_qr_code.html',context=context)        
    else:
        return redirect('login')
    







def verify_qr_code(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
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
            pass
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
        item=[]
        if e:
            v = Voucher_name.objects.get(id=id)
            q = Out_item.objects.filter(voucher_id=id).order_by('item_id')
            a = Out_item.objects.filter(voucher_id=id,verify_status=1).count()
            b = Out_item.objects.filter(voucher_id=id).count()
            ite = Item.objects.all()
            if ite :
                for ite in ite :
                    itm=Out_item.objects.filter(voucher_id=id,item_id=ite.id).first()
                    if itm:
                        item.append(itm)
            if 'Verify' in request.POST:
                item_id = request.POST.get('item_id')
                qr = Out_item.objects.filter(voucher_id=id,item_id=item_id,verify_status=0)
                if qr:
                    for q in qr:
                        q.verify_status = 1 
                        q.verify_by_id = e.id
                        q.verify_date = datetime.datetime.now()
                        q.save()
                return redirect(f'/office/pending_view_voucher/{id}')
            if 'Voucher_Verify' in request.POST:
                v = Voucher_name.objects.get(id=id)
                v.verify_by_id = e.id
                v.verify_status = 1
                v.verify_date = datetime.datetime.now()
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
            'q':item,
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
            v = Voucher_name.objects.get(id=id)
            q = Out_item.objects.filter(voucher_id=id).order_by('item_id')
        context={
            'e':e,
            'v':v,
            'q':q

        }
        return render(request,'office/accepted_view_voucher.html',context=context)        
    else:
        return redirect('login')


    
def report(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={
            'e':e,
        }
        return render(request,'office/report.html',context=context)        
    else:
        return redirect('login')

def in_report(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            s = Shift.objects.all().order_by('-id')
            paginator = Paginator(s,1000) 
            page_number = request.GET.get('page')
            s = paginator.get_page(page_number)
            total_pages = s.paginator.num_pages
        context={
            'e':e,
            's': s,
            'last_page':total_pages,
            'total_page_list':[n+1 for n in range(total_pages)][0:3]
        }
        return render(request,'office/in_report.html',context=context)        
    else:
        return redirect('login')


def out_report(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={
            'e':e,
        }
        return render(request,'office/out_report.html',context=context)        
    else:
        return redirect('login')


def shift_detail(request, shift_id):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        in_item = []
        helper = []
        if e:
            shift = Shift.objects.get(id=shift_id)
            in_item_count = In_item.objects.filter(shift_id=shift.id).count()
            item = Item.objects.all()
            if item:
                for i in item:
                    it = In_item.objects.filter(item_id = i.id,operator_id=e.id,shift_id = shift.id).first()
                    if it:
                        in_item.append(it)
            in_employee = In_employee.objects.all()
            if in_employee:
                for ie in in_employee:
                    he = In_item.objects.filter(in_employee_id=ie.id,operator_id=e.id,shift_id = shift.id).first()
                    if he:
                        helper.append(he)
        context={
                'e':e,
                'shift':shift,
                'in_item_count':in_item_count,
                'in_item':in_item,
                'helper':helper
        }
        return render(request,'office/shift_detail.html',context=context)        
    else:
        return redirect('login')
    
 
def billing(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']        
        e=Employee.objects.filter(mobile=office_mobile).first()
        if e:
            pass
        context={
            'e':e,
            'bill':Billing.objects.all()
        }
        return render(request,'office/billing.html',context=context)        
    else:
        return redirect('login')





  