from django.test import TestCase

# Create your tests here.


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
