from django.shortcuts import render
from office.models import *
from django.template.loader import render_to_string
from django.http import *
from store.models import *
from datetime import *
from django.contrib import messages
# Create your views here.
def search_batch_item(request):
    if request.method == 'GET':
        words = request.GET['words']
        p=Item.objects.filter(name__icontains=words)
        context={
                's_p':p
        }
        t = render_to_string('ajax/office/search_batch_item.html', context)
    return JsonResponse({'data': t})

def fetch_batch(request):
    if request.method == 'GET':
        pid = request.GET['pid']
        pro = Item.objects.get(id=pid)
        ba = Batch.objects.filter(item_id=pid)
        context={
            'pro':pro,
            'ba':ba
        }
        t = render_to_string('ajax/office/fetch_batch.html', context)
    return JsonResponse({'t': t})


def batch_detail(request):
    if request.method == 'GET':
        bid = request.GET['bid']
        ba = Batch.objects.get(id=bid)
        un_used = Qr_code.objects.filter(batch_id=bid,in_status=0).count()
        in_stock = Qr_code.objects.filter(batch_id=bid,in_status=1,out_status=0).count()
        out_stock = Qr_code.objects.filter(batch_id=bid,in_status=1,out_status=1).count()
        qr_code = Qr_code.objects.filter(batch_id=bid).order_by('-in_status' ,'out_status')

        context={
            'ba':ba,
            'un_used':un_used,
            'in_stock':in_stock,
            'out_stock':out_stock,
            'qr_code':qr_code
            }
        t = render_to_string('ajax/office/batch_detail.html', context)
    return JsonResponse({'t': t}) 







def add_new_batch(request):
    if request.method == 'GET':
        batch_name = request.GET['batch_name']
        eid = request.GET['eid']
        pid = request.GET['pid']
        sr = Batch.objects.filter(item_id=pid).count()
        sr += 1
        if batch_name == '':
            pass
        else:
            Batch(
                batch_name=batch_name,
                employee_id=eid,
                item_id=pid,
                sr_num=sr,
            ).save()
        b = Batch.objects.filter(item_id=pid)

        context={
            'b':b
        }
        t = render_to_string('ajax/office/batch_history.html', context)
    return JsonResponse({'data': t}) 


def search_qr_item(request):
    if request.method == 'GET':
        words = request.GET['words']
        p=Item.objects.filter(name__icontains=words)
        context={
                's_p':p
        }
        t = render_to_string('ajax/office/search_qr_item.html', context)
    return JsonResponse({'data': t})

def multiple_tage(request):
    if request.method == 'GET':
        status = 0
        qr = ''
        batch_id = request.GET['batch_id']
        eid = request.GET['eid']
        tag_qty = request.GET['tag_qty']
        b = Batch.objects.get(id=batch_id)
        t = Qr_code.objects.filter(batch_id=batch_id,item_id=b.item_id).count()
        t += 1
        p_id = b.item_id
        if int(t) < 1001:
            for i in range (int(tag_qty)):
                f = f'{p_id}{batch_id}{t}'
                Qr_code(
                    item_id=b.item_id,
                    employee_id=eid,
                    batch_id=b.id,
                    tag_number=f,
                    sr_num=t
                    ).save() 
                t += 1
        else:
            status = 1
        qr = Qr_code.objects.filter(batch_id=batch_id).order_by('-id')
        tag = Qr_code.objects.filter(batch_id=batch_id,item_id=b.item_id).order_by('-id')[0:int(tag_qty)]
        context={
            'qr':qr
        }
        contex2={
            'tag':tag
        }
        t = render_to_string('ajax/office/tag_list.html', context)
        multiple_tag_generate = render_to_string('ajax/office/multiple_tag_generate.html', contex2)
    return JsonResponse({'t':t,'tag':multiple_tag_generate ,'status':status}) 



def in_item(request):
    if request.method == 'GET':
        tag_num = request.GET['tag_num']
        eid = request.GET['e_id']
        ti_item=[]
        status = ''
        i_name = ''
        #print('tag_num = ',tag_num,  'eid = ',eid)
        qr = Qr_code.objects.filter(tag_number=tag_num).first()
        if qr:
            i_name = qr.item.name
            if qr.in_status == 0 and qr.out_status == 0:
                in_item_save(tag_num,eid,scan_type=1)
                i=Item.objects.all()
                for i in i:
                    i_all_id = i.id
                    ti = In_item.objects.filter(item_id=i_all_id,date__gte=date.today(),date__lte=date.today()).order_by('-id').first()
                    if ti:
                        ti_item.append(ti)
                status = 1

            if qr.in_status == 1:
                status = 2
        else:
            status = 0
        context={
            'i':ti_item
                }
        t = render_to_string('ajax/store/today_production.html', context)
    return JsonResponse({'status':status,'i_name':i_name, 't':t}) 

def in_item_manual(request):
    if request.method == 'GET':
        tag_num = request.GET['tag_num']
        eid = request.GET['e_id']
        ti_item=[]
        status = ''
        i_name = ''
        #print('tag_num = ',tag_num,  'eid = ',eid)
        qr = Qr_code.objects.filter(tag_number=tag_num).first()
        if qr:
            i_name = qr.item.name
            if qr.in_status == 0 and qr.out_status == 0:
                in_item_save(tag_num,eid,scan_type=0)
                i=Item.objects.all()
                for i in i:
                    i_all_id = i.id
                    ti = In_item.objects.filter(item_id=i_all_id,date__gte=date.today(),date__lte=date.today()).order_by('-id').first()
                    if ti:
                        ti_item.append(ti)
                status = 1

            if qr.in_status == 1:
                status = 2
        else:
            status = 0
        context={
            'i':ti_item
                }
        t = render_to_string('ajax/store/today_production.html', context)
    return JsonResponse({'status':status,'i_name':i_name, 't':t}) 

def in_item_save(tag,eid,scan_type):
    #print('tag_num = ',tag,  'eid = ',eid,  'scan_type = ', scan_type)
    qr = Qr_code.objects.get(tag_number=tag,in_status=0)
    if qr:
        In_item(
            employee_id = eid,
            qr_code_id = qr.id,
            item_id = qr.item_id,
            tag_number = tag,
            status = 1,
            scan_type=scan_type,
        ).save()
        qr.in_status = 1
        qr.save()
    

def search_tag(request):
    if request.method == 'GET':
        tag_num = request.GET['tag_num']
        item = ''
        i = Qr_code.objects.filter(tag_number=tag_num).first()
        if i:
            item = Qr_code.objects.filter(tag_number=tag_num).first()
        context={
            'i':item
               }
        t = render_to_string('ajax/store/serch_in_tag_result.html', context)
    return JsonResponse({'t':t}) 

def search_out_tag(request):
    if request.method == 'GET':
        tag_num = request.GET['tag_num']
        item = ''
        i = Qr_code.objects.filter(tag_number=tag_num).first()
        if i:
            item = Qr_code.objects.filter(tag_number=tag_num).first()
        context={
            'i':item
               }
        t = render_to_string('ajax/store/serch_out_tag_result.html', context)
    return JsonResponse({'t':t}) 


def out_item(request):
    if request.method == 'GET':
        status = ''
        i_name = ''
        vi_item = []
        tag_num = request.GET['tag_num']
        em_id = request.GET['e_id']
        v_id = request.GET['vid']
        if tag_num:
            qr = Qr_code.objects.filter(tag_number=tag_num).first()
            if qr:
                i_name = qr.item.name
                if qr.in_status == 1 and qr.out_status == 0:
                    #Out sucess
                    out_item_save(tag_num,em_id,v_id,scan_type=1)
                    it = Item.objects.all()
                    for i in it:
                        vi = Out_item.objects.filter(voucher_id=v_id,item_id=i.id).first()
                        if vi:
                            vi_item.append(vi)
                    status = 1
                if qr.in_status == 0:
                    #First Add Production
                    status = 2
                if qr.in_status == 1 and qr.out_status == 1:
                    #Already scaned
                    status = 3
            else:
                #Rong Qrcode
                status = 0
            context={
                'vi_item':vi_item
            }
        t = render_to_string('ajax/store/out_tag_list.html', context)
    return JsonResponse({'t':t,'status':status,'i_name':i_name}) 


def out_item_save(tag_num,em_id,v_id,scan_type):
    qr = Qr_code.objects.filter(tag_number=tag_num).first()
    if qr:
        Out_item(
            employee_id=em_id,
            qr_code_id=qr.id,
            item_id=qr.item_id,
            voucher_id=v_id,
            tag_number=tag_num,
            scan_type=scan_type,
        ).save()
        qr.out_status = 1
        qr.save()
        ins = In_item.objects.get(tag_number=tag_num)
        ins.status = 0
        ins.save()


def out_item_manual(request):
    if request.method == 'GET':
        status = ''
        i_name = ''
        vi_item = []
        tag_num = request.GET['tag_num']
        em_id = request.GET['e_id']
        v_id = request.GET['vid']
        if tag_num:
            qr = Qr_code.objects.filter(tag_number=tag_num).first()
            if qr:
                i_name = qr.item.name
                if qr.in_status == 1 and qr.out_status == 0:
                    #Out sucess
                    out_item_save(tag_num,em_id,v_id,scan_type=0)
                    it = Item.objects.all()
                    for i in it:
                        vi = Out_item.objects.filter(voucher_id=v_id,item_id=i.id).first()
                        if vi:
                            vi_item.append(vi)
                    status = 1
                if qr.in_status == 0:
                    #First Add Production
                    status = 2
                if qr.in_status == 1 and qr.out_status == 1:
                    #Already scaned
                    status = 3
            else:
                #Rong Qrcode
                status = 0
            context={
                'vi_item':vi_item
            }
        t = render_to_string('ajax/store/out_tag_list.html', context)
    return JsonResponse({'t':t,'status':status,'i_name':i_name}) 



def search_item(request):
    if request.method == 'GET':
        words = request.GET['words']
        p = ''
        if len(words) > 2:
            p=Item.objects.filter(name__icontains=words)[0:10]
        context={
            'pro':p
        }
        t = render_to_string('ajax/office/search_item.html', context)
    return JsonResponse({'t': t})