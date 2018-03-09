from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('despesa/', views.cadastro_despesa, name='cadastro_despesa'),
    path('despesa/<int:despesa_id>/contas/cadastro', views.cadastro_conta, name='cadastro_conta'),
    path('', views.listar_contas, name='index'),
    path('despesa/<int:despesa_id>/contas/', views.listar_contas_depesa, name='listar_contas_depesa'),
    path('despesa/<int:despesa_id>/conta/<int:conta_id>/pagar/', views.pagar_conta, name='pagar_conta'),
    path('despesa/<int:despesa_id>/contas/cadastro/sucesso/', views.contas_cadastradas_sucesso, name='contas_cadastradas_sucesso'),
    path('despesa/<int:despesa_id>/alteracao/', views.alteracao_despesa, name='alteracao_despesa'),
]
