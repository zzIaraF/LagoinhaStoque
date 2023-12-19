from django.contrib import admin

from .models import Fornecedor
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['id', 'razaosocial',  'cnpj', 'endereco', 'telefone', 'data']
    list_display_links = ['id', 'razaosocial']
    list_per_page = 5


# # Register your models here.
admin.site.register(Fornecedor, FornecedorAdmin)
