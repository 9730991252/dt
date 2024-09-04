from django.urls import path
from office import views
urlpatterns = [
    path('office_dashboard/', views.office_dashboard, name='office_dashboard'),
    path('employee/', views.employee, name='employee'),
    path('item/', views.item, name='item'),
    path('generate_qr_code', views.generate_qr_code,name='generate_qr_code'),
    path('verify_qr_code', views.verify_qr_code,name='verify_qr_code'),
    path('pending_verify_qr_code', views.pending_verify_qr_code,name='pending_verify_qr_code'),
    path('pending_view_voucher/<int:id>', views.pending_view_voucher,name='pending_view_voucher'),
    path('accepted_verify_qr_code', views.accepted_verify_qr_code,name='accepted_verify_qr_code'),
    path('accepted_view_voucher/<int:id>', views.accepted_view_voucher,name='accepted_view_voucher'),
    path('report/', views.report,name='report'),
    path('in_report/', views.in_report,name='in_report'),
    path('out_report/', views.out_report,name='out_report'),
    path('shift_detail/<int:shift_id>', views.shift_detail,name='shift_detail'),
    path('billing/', views.billing,name='billing'),
]