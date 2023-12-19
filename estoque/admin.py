from django.contrib import admin

from .models import Categoria, Produto
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_display_links = ['id', 'nome']
    list_per_page = 10

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'categoria', 'preco', 'precovenda', 'estoque', 'estoquemin', 'usuario', 'fornecedor']
    list_display_links = ['id', 'nome']
    list_per_page = 5

# # Register your models here.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
