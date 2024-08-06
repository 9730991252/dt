from django.shortcuts import render , redirect
from django.contrib import messages
from office.models import *
from store.models import *
# Create your views here.
def index(request):
    #Qr_code.objects.all().delete()
    #Batch.objects.all().delete()
    #Item.objects.all().delete()
    #Voucher_name.objects.filter(verify_status=1).delete()
    return render(request, 'home/index.html')

def login(request):
    if request.session.has_key('office_mobile'):
        return redirect('office_dashboard')
    if request.session.has_key('store_mobile'):
        return redirect('store_dashboard')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            e= Employee.objects.filter(mobile=number,pin=pin,status=1,department='office')
            if e:
                request.session['office_mobile'] = request.POST["number"]
                return redirect('office_dashboard')
            s= Employee.objects.filter(mobile=number,pin=pin,status=1,department='store')
            if s:
                request.session['store_mobile'] = request.POST["number"]
                return redirect('store_dashboard')
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

def store_logout(request):
    del request.session['store_mobile']
    return redirect('login')