from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('owner/login/', views.owner_login, name='owner_login'),
    path('owner/register/', views.owner_register, name='owner_register'),
    path('owner/logout/', views.owner_logout, name='owner_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('owner_dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('printer/', views.printer, name='printer'),
    path('printer/<int:pid>/', views.printer_detail, name='printer_detail'),
    path('printer/create/', views.printer_create, name='printer_create'),
    path('printer/<int:pid>/edit/', views.printer_edit, name='printer_edit'),
    path('printer/<int:pid>/delete/', views.printer_delete, name='printer_delete'),
    path('appointment/create/', views.appointment_create, name='appointment_create'),
    path('appointment/list/', views.appointment_list, name='appointment_list'),
    path('appointment/<int:appointmentId>/', views.appointment_detail, name='appointment_detail'),
    path('appointment/<int:appointmentId>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointment/<int:appointmentId>/delete/', views.appointment_delete, name='appointment_delete'),
    path('appointment/<int:appointmentId>/approve/', views.approve_appointment, name='approve_appointment'),
    path('appointment/<int:appointmentId>/disapprove/', views.disapprove_appointment, name='disapprove_appointment'),
    
]

