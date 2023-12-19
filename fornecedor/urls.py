from django.urls import path

from . import views
urlpatterns = [
    path('fornecedor/', views.cadastrarfornecedor, name= "cadastrarfornecedor"),
    path('listarfornecedor/', views.listarfornecedor, name='listarfornecedor'),
    path('editar_fornecedor/<int:fornecedor_id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedor/<int:fornecedor_id>/', views.exibirfornecedor, name="exibirfornecedor"),
    path('inativar_fornecedor/<int:fornecedor_id>/', views.inativar_fornecedor, name='inativar_fornecedor'),
     path('ativar_fornecedor/<int:fornecedor_id>/', views.ativar_fornecedor, name='ativar_fornecedor'),
   

    

]
