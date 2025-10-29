
from django.urls import path
from home.views import *
from . import views

urlpatterns = [
    path('',homefn),
    path('aboutus/',aboutusfn),
    path('ourlocation/',locationfn),
    path('services/',servicesfn),
    path('booking/', views.booking_view, name='booking'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('contact/', views.contact_view, name='contact'),
    path("login/", views.login_view, name="login"),
    path('admindashboard/', views.admindashboardfn, name='admin_dashboard'),
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path("doctor/add/", views.add_doctor, name="add_doctor"),
    path("doctor/edit/<int:doctor_id>/", views.edit_doctor, name="edit_doctor"),
    path("doctor/delete/<int:doctor_id>/", views.delete_doctor, name="delete_doctor"),
    path("appointment/confirm/<int:appointment_id>/", views.confirm_appointment, name="confirm_appointment"),
    path("appointment/cancel/<int:appointment_id>/", views.cancel_appointment, name="cancel_appointment"),
    path("appointments/add/", views.add_appointment, name="add_appointment"),
    path('dashboard/delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
   
   
    


   
    
    
   
    
    
    
   
    

    
]
   

