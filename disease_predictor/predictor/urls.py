from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view,name='home'),
    path('diagnoser/', views.diagnoser_view,name='diagnoser'),
]
