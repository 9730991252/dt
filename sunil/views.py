from django.shortcuts import render, redirect, HttpResponse
from office.models import *
from store.models import *
from .models import *
from django.contrib import messages
from datetime import timedelta, date
# Create your views here.
def add_employee_sunil(request):
    if request.session.has_key('sunil_mobile'):
        context={}
        if 'add_employee'in request.POST:
            name=request.POST.get('name')
            mobile=request.POST.get('mobile')
            pin=request.POST.get('pin')
            if Employee.objects.filter(mobile=mobile).exists():
                messages.success(request,"Employee Allready Exits")
            else:
                Employee(
                    name=name,
                    mobile=mobile,
                    pin=pin,
                    ).save()
                messages.success(request,"Employee Add Succesfully") 
                return redirect('add_employee_sunil')
        context={
            'e':Employee.objects.all()
        }
        return render(request, 'sunil/add_employee_sunil.html', context)
    else:
        return redirect('sunil_login')
    
def billing(request):
    if request.session.has_key('sunil_mobile'):
        context={}
        from_date=''
        to_date=''
        in_count=''
        out_count=''
        total=''
        if 'Search'in request.POST:
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            #print('from_date =',from_date ,'to_date = ',to_date )
            in_count = In_item.objects.filter(date__gte=from_date,date__lte=to_date).count()
            out_count = Out_item.objects.filter(date__gte=from_date,date__lte=to_date).count()
            total = (in_count + out_count)* 0.10 + 2000
        
        elif 'Generate_bill'in request.POST:
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            in_count = In_item.objects.filter(date__gte=from_date,date__lte=to_date).count()
            out_count = Out_item.objects.filter(date__gte=from_date,date__lte=to_date).count()
            total = (in_count + out_count)* 0.10 + 2000
            if Billing.objects.filter(from_date=from_date,to_date=to_date).exists():
                messages.warning(request,"Bill Allready Exits")
            else :
                Billing(
                    from_date=from_date,
                    to_date=to_date,
                    total_in=in_count,
                    total_out=out_count,
                    hosting=2000,
                    total=total,
                    ).save()
                messages.success(request,"Bill Generated Bill")
                return redirect('/sunil/billing/')
        elif 'Pay_bill'in request.POST:
                bill_id=request.POST.get('bill_id')
                b=Billing.objects.get(id=bill_id)
                b.status=1
                b.paid_date=date.today()
                b.save()     
                return redirect('/sunil/billing/')
        context={
            'from_date':from_date,
            'to_date':to_date,
            'date_today':date.today(),
            'in_count':in_count,
            'out_count':out_count,
            'total':total,
            'un_paid':Billing.objects.filter(status=0),
            'paid':Billing.objects.filter(status=1)

                }
        return render(request, 'sunil/billing.html', context)
    else:
        return redirect('sunil_login')
    
     