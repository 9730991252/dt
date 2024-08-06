from django.urls import path
from ajax import views
urlpatterns = [
    path('search_batch_item', views.search_batch_item,name='search_batch_item'),
    path('add_new_batch', views.add_new_batch,name='add_new_batch'),
    path('search_qr_item', views.search_qr_item,name='search_qr_item'),
    path('multiple_tage', views.multiple_tage,name='multiple_tage'),
    path('in_item', views.in_item,name='in_item'),
    path('search_tag', views.search_tag,name='search_tag'),
    path('search_out_tag', views.search_out_tag,name='search_out_tag'),
    path('in_item_manual', views.in_item_manual,name='in_item_manual'),
    path('out_item', views.out_item,name='out_item'),
    path('out_item_manual', views.out_item_manual,name='out_item_manual'),
    path('fetch_batch', views.fetch_batch,name='fetch_batch'),
    path('batch_detail', views.batch_detail,name='batch_detail'),
    path('search_item', views.search_item,name='search_item'),
        ]