from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register', views.register_info),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('sports/new', views.new_sport),
    path('create/sport', views.create_sport),
    path('sports/remove/<int:sport_id>', views.remove_sport),
    path('sports/edit/<int:sport_id>', views.edit_sport),
    path('sports/update/<int:sport_int>', views.update_sport),
    
]