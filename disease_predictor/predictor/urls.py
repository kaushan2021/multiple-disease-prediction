from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view,name='home'),
    path('diagnoser/', views.diagnoser_view,name='diagnoser'),
    path('breast_cancer_prediction/', views.breast_cancer_prediction,name='breast_cancer_prediction'),
    path('breast_cancer_info/', views.breast_cancer_info__view,name='breast_cancer_info'),
    path('specialist_consultant/', views.specialist_consultant__view,name='specialist_consultant'),
    path('heart_disease_prediction/', views.heart_disease_prediction,name='heart_disease_prediction'),
    path('parkinsons_prediction/', views.parkinsons_prediction,name='parkinsons_prediction'),
    path('heart_disease_info/', views.heart_disease_info_view,name='heart_disease_info'),
    path('parkinsons_disease_info/', views.parkinsons_disease_info_view,name='parkinsons_disease_info'),
    path('login/', views.user_login_form, name='login_form'),
    path('login_authenticate/', views.user_login, name='login'),
    path('user_reg/', views.user_reg_form, name='user_reg_form'),
    path('patient_create/', views.create_patient, name='create_patient'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('create_gp/', views.create_gp, name='create_gp'),
    path('gp_reg_form/', views.user_reg_form, name='gp_reg_form'),

]

