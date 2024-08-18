from datetime import date
from store.models import *
from django import template
register = template.Library()
 
@register.simple_tag
def today_production(id):
    qty = In_item.objects.filter(item_id=id,date__gte=date.today(),date__lte=date.today()).count()
    return qty

@register.inclusion_tag('inclusion_tag/store/today_production_tag.html')
def today_production_tag(id):
    tag = In_item.objects.filter(item_id=id,date__gte=date.today(),date__lte=date.today()).order_by('tag_number')
    return {
        'tag':tag
    } 

@register.simple_tag
def out_item_total(v_id,i_id):
    return Out_item.objects.filter(voucher_id=v_id,item_id=i_id).count()


@register.inclusion_tag('inclusion_tag/store/out_tag_list.html')
def out_tag_list(v_id,i_id):
    tag = Out_item.objects.filter(voucher_id=v_id,item_id=i_id).order_by('-tag_number')
    return {
        'tag':tag
    } 


@register.simple_tag
def today_production_employee(id, e_id, shift_id):
    if shift_id :
        qty = In_item.objects.filter(item_id=id,in_employee_id=e_id,shift_id=shift_id).count()
        return qty

@register.simple_tag
def today_production_machine(m_id,shift_id):
    if shift_id:
        qty = In_item.objects.filter(machine_id=m_id,shift_id=shift_id).count()
        return qty

 
@register.inclusion_tag('inclusion_tag/store/today_production_tag.html')
def today_production_in_tag(id, e_id,shift_id):
    if shift_id :
        tag = In_item.objects.filter(item_id=id,shift_id=shift_id,in_employee_id=e_id).order_by('-tag_number')
        return {
            'tag':tag
        } 
 
@register.simple_tag
def hide_operator_item(item_id, operator_id, ):
    #print('item_id =', item_id , 'operator_id =', operator_id)
    s = Select_operator_item.objects.filter(operator_id=operator_id,item_id=item_id).first()
    if s:
        return True


@register.simple_tag
def operator_production(item_id, operator_id, shift_id):
    if shift_id :
        qty = In_item.objects.filter(item_id=item_id,operator_id=operator_id,shift_id=shift_id).count()
        return qty

@register.inclusion_tag('inclusion_tag/store/operator/operator_production_list.html')
def operator_production_list(item_id, operator_id, shift_id):
    if shift_id :
        tag = In_item.objects.filter(item_id=item_id,operator_id=operator_id,shift_id=shift_id).order_by('-tag_number')
        return {
            'tag':tag
        }

@register.simple_tag
def helper_production(helper_id, shift_id):
    print('yes',helper_id)
    if shift_id :
        qty = In_item.objects.filter(in_employee_id=helper_id,shift_id=shift_id).count()
        return qty

@register.inclusion_tag('inclusion_tag/store/operator/operator_production_list.html')
def helper_production_list(helper_id, shift_id):
    if shift_id :
        tag = In_item.objects.filter(in_employee_id=helper_id,shift_id=shift_id).order_by('-tag_number')
        return {
            'tag':tag
        }

@register.simple_tag
def operator_all_production(operator_id, shift_id):
    if shift_id :
        qty = In_item.objects.filter(operator_id=operator_id,shift_id=shift_id).count()
        return qty

