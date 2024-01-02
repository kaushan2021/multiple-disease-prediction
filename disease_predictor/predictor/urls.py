from django.urls import path
from . import views

urlpatterns = [
    path('breast-cancer-prediction/', views.breast_cancer_prediction,name='breast_cancer_prediction'),
    path('', views.home_view,name='home'),
]
