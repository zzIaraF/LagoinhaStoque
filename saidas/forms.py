from django import forms
from .models import Saidas
from estoque.models import Produto
from django.utils import timezone
from django.core.exceptions import ValidationError


class SaidasForm(forms.ModelForm):
    class Meta:
        model = Saidas
        fields = ['nomedoproduto', 'quantidade', 'data']
 

    nomedoproduto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),  
        empty_label="Selecione um produto",  
        label='Nome do Produto'
    )
def clean_quantidade(self):
    quantidade = self.cleaned_data['quantidade']
    if quantidade <= 0:
        print('DEBUG: Quantidade menor ou igual a zero')
        raise forms.ValidationError('A quantidade deve ser maior que zero')
    return quantidade

def clean_data(self):
        data = self.cleaned_data['data']
        if data and data > timezone.now().date():
            raise ValidationError('A data não pode estar no futuro.')
        return data


