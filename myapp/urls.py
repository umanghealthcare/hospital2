from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('doctor/',views.doctor,name='doctor'),
    path('service/',views.service,name='service'),
    path('appoinment/',views.appoinment,name="appoinment"),
    path('confirmation/',views.confirmation,name="confirmation"),
    path('doctor_single/<int:pk>',views.doctor_single,name="doctor_single"),
    path('service/',views.service,name="service"),
    path('header/',views.header,name="header"),
    path('about/',views.about,name="about"),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.logout,name="logout"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('change_pass/',views.change_pass,name='change_pass'),
    path('doctor_index/',views.doctor_index,name='doctor_index'),
    path('doctor_header/',views.doctor_header,name='doctor_header'),
    path('doctor_persional_profile/',views.doctor_persional_profile,name='doctor_persional_profile'),
    path('doctor_office_details/',views.doctor_office_details,name='doctor_office_details'),
    path('doctor_change_pass/',views.doctor_change_pass,name='doctor_change_pass'),
    path('makeappointment/<int:pk>/',views.makeappointment,name='makeappointment'),
    path('myappointment/',views.myappointment,name='myappointment'),
    path('doctor_appointment/',views.doctor_appointment,name='doctor_appointment'),
    path('patient_appointments_cancel/<int:pk>/',views.patient_appointments_cancel,name='patient_appointments_cancel'),
    path('appcept_request/<int:pk>/',views.appcept_request,name='appcept_request'),
    path('doctor_appointment_cancel/<int:pk>/',views.doctor_appointment_cancel,name='doctor_appointment_cancel'),
    path('ajax/validate_email/',views.validate_signup,name='validate_email'),
    path('pay/<int:pk>/',views.initiate_payment, name='pay'),
    path('callback/',views.callback, name='callback'),
    path('health_profile/',views.health_profile,name='health_profile'),
    path('doctor_patient_report/<int:pk>/',views.doctor_patient_report,name='doctor_patient_report'),
    path('prescription_by_doctor/<int:pk>/',views.prescription_by_doctor,name='prescription_by_doctor'),
    path('prescription_by_doctor_patient/<int:pk>/',views.prescription_by_doctor_patient,name='prescription_by_doctor_patient'),
    path('print_appointment/<int:pk>/',views.print_appointment,name='print_appointment'),
    path('project/',views.project,name='project'),

]







