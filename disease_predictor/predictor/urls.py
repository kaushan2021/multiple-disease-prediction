from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view,name='home'),
    path('diagnoser/', views.diagnoser_view,name='diagnoser'),
    path('breast_cancer_prediction/', views.breast_cancer_prediction,name='breast_cancer_prediction'),
    path('breast_cancer_info/', views.breast_cancer_info__view,name='breast_cancer_info'),
    path('specialist_consultant/', views.specialist_consultant__view,name='specialist_consultant'),
]

