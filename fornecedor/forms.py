from django import forms
from .models import Fornecedor

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['razaosocial', 'cnpj', 'telefone', 'data','endereco','ativo']
