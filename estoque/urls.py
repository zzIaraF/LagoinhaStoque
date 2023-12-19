from django.urls import path

from . import views

urlpatterns = [
    path('cadastro/', views.add_produtos, name="add_produtos"),
    path('listar/', views.listaProdutos, name= "listaProdutos"),
    path('<int:produto_id>/<int:fornecedor_id>/', views.prod_exibir, name="prod_exibir"),
    path('editar/<int:produto_id>', views.editarProdutos, name="editarProdutos"),
  
    path('categorias/cadastro/', views.cadastrarCategorias, name="cadastro_categorias"),
    path('categorias/', views.listaCategorias, name='listagem_categorias'),
    path('categorias/editar/<int:categoria_id>/', views.cat_editar, name='editar_categorias'),
    path('categorias/excluir/<int:id>/', views.cat_excluir, name='excluir_categorias'),
]