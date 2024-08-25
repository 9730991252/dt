from django.urls import path
from store import views
urlpatterns = [
    path('in_home/', views.in_home, name='in_home'),
    path('out_home/', views.out_home, name='out_home'),
    path('search_in_item/', views.search_in_item, name='search_in_item'),
    path('item_in/<int:item_id>', views.item_in, name='item_in'),
    path('add_voucher/', views.add_voucher, name='add_voucher'),
    path('item_out/<int:id>', views.item_out, name='item_out'),
    path('operator_home/', views.operator_home, name='operator_home'),
    path('operator_shift/', views.operator_shift, name='operator_shift'),
    path('select_helper/<int:shift_id>', views.select_helper, name='select_helper'),
]