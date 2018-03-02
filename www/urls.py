from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('despesa/', views.cadastro_despesa, name='cadastro_despesa'),
    path('despesa/<int:despesa_id>/contas/cadastrar', views.cadastro_conta, name='cadastro_conta'),
    path('', views.listar_contas, name='index'),
    path('despesa/<int:despesa_id>/contas/', views.listar_contas_depesa, name='listar_contas_depesa'),
    path('hero/', views.hero, name='hero'),
]
