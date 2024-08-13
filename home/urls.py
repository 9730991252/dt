from django.urls import path
from home import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('sunil_login/', views.sunil_login, name='index'),
    path('office_logout/', views.office_logout, name='office_logout'),
    path('in_logout/', views.in_logout, name='in_logout'),
    path('out_logout/', views.out_logout, name='out_logout'),
    path('operator_logout/', views.operator_logout, name='operator_logout'),
]