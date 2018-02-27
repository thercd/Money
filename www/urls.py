from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.cadastro_despesa, name='cadastro_despesa'),
    path('hero/', views.hero, name='hero'),
]
