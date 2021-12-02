from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register', views.register_info),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('sports/new', views.new_sport),
    path('create/sport', views.create_sport),
]