from django import forms
from .models import Produto

class ProdutosForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'ncm', 'categoria', 'preco', 'precovenda', 'estoque', 'estoquemin', 'usuario', 'fornecedor']