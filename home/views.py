from django.shortcuts import render , redirect
from django.contrib import messages
from office.models import *
from store.models import *
# Create your views here.
def index(request):
    #Out_item.objects.all().delete()
    #Voucher_name.objects.all().delete()
    #In_item.objects.all().delete()
    #Qr_code.objects.all().delete()
    #Batch.objects.all().delete()
    #Item.objects.all().delete()
    #Operator.objects.all().delete()
    #Shift.objects.all().delete()

    #******************

    #m = Machine.objects.filter(working_status=1).first()
    #m.working_status = 0
    #m.save()
    return render(request, 'home/index.html')

def login(request):
    if request.session.has_key('office_mobile'):
        return redirect('office_dashboard')
    if request.session.has_key('in_mobile'):
        return redirect('in_home')
    if request.session.has_key('out_mobile'):
        return redirect('out_home')
    if request.session.has_key('operator_mobile'):
        return redirect('operator_home')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            e= Employee.objects.filter(mobile=number,pin=pin,status=1)
            if e:
                request.session['office_mobile'] = request.POST["number"]
                return redirect('office_dashboard')
            ie= In_employee.objects.filter(mobile=number,pin=pin,status=1)
            if ie:
                request.session['in_mobile'] = request.POST["number"]
                return redirect('in_home')
            oe= Out_employee.objects.filter(mobile=number,pin=pin,status=1)
            if oe:
                request.session['out_mobile'] = request.POST["number"]
                return redirect('out_home')
            op = Operator.objects.filter(mobile=number,pin=pin,status=1)
            if op:
                request.session['operator_mobile'] = request.POST["number"]
                return redirect('operator_home')
            else:
                messages.success(request,"please insert correct information or call more suport 9730991252")            
                return redirect('login')
    return render(request, 'home/login.html')



def sunil_login(request):
    if request.method == 'POST':
        a =int(request.POST["number"])
        b =int(request.POST["pin"])
        s = a+b
        if s == 10000 :
            request.session['sunil_mobile'] = s
            return redirect('add_employee_sunil')
        else:
            return redirect('sunil_login')
    return render(request,'home/sunil_login.html')

def office_logout(request):
    del request.session['office_mobile']
    return redirect('login')

def in_logout(request):
    del request.session['in_mobile']
    return redirect('login')

def out_logout(request):
    del request.session['out_mobile']
    return redirect('login')

def operator_logout(request):
    del request.session['operator_mobile']
    return redirect('login')