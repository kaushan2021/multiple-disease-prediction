from django.urls import path
from . import views

urlpatterns = [
    path('gp_home/', views.gp_home_view,name='gp_home'),
    path('diagnoser/', views.diagnoser_view,name='diagnoser'),
    path('breast_cancer_prediction/', views.breast_cancer_prediction,name='breast_cancer_prediction'),
    path('breast_cancer_info/', views.breast_cancer_info__view,name='breast_cancer_info'),
    path('specialist_consultant/', views.specialist_consultant__view,name='specialist_consultant'),
    path('heart_disease_prediction/', views.heart_disease_prediction,name='heart_disease_prediction'),
    path('parkinsons_prediction/', views.parkinsons_prediction,name='parkinsons_prediction'),
    path('heart_disease_info/', views.heart_disease_info_view,name='heart_disease_info'),
    path('parkinsons_disease_info/', views.parkinsons_disease_info_view,name='parkinsons_disease_info'),
    path('', views.user_login_form, name='login_form'),
    path('login_authenticate/', views.user_login, name='login'),
    path('user_reg/', views.user_reg_form, name='user_reg_form'),
    path('patient_create/', views.create_patient, name='create_patient'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('create_gp/', views.create_gp, name='create_gp'),
    path('gp_reg_form/', views.user_reg_form, name='gp_reg_form'),
    path('medical_specialist_create/', views.create_medical_specialist, name='create_medical_specialist'),
    path('medical_specialist_reg_form/', views.user_reg_form, name='medical_specialist_reg_form'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_home/', views.admin_home_view, name='admin_home_view'),
    path('gp_patient_select/', views.gp_patient_select, name='gp_patient_select'),
    path('logout/', views.log_out, name='logout'),
    path('patient_home/', views.patient_home, name='patient_home'),
    path('patient_notification/', views.patient_notification, name='patient_notification'),
    path('patient_appointment_scheduler/', views.patient_appointment_scheduler, name='patient_appointment_scheduler'),
    path('desease_education/', views.desease_education, name='desease_education'),
    path('patient_report_result/', views.patient_report_result, name='patient_report_result'),
    path('appointment_scheduler/', views.appointment_scheduler, name='appointment_scheduler'),
    path('specialist_home/', views.specialist_home, name='specialist_home'),
    path('specialist_appoinments/', views.specialist_appoinments, name='specialist_appoinments'),
    path('specialist_report/', views.specialist_report_view, name='specialist_report'),
    path('medical_history/', views.medical_history, name='medical_history')
    
]

