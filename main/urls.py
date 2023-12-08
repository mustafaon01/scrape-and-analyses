from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('read-me/', views.read_me, name='read-me'),
]

