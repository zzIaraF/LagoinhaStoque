from django.db import models
from django.contrib.auth.models import User
from fornecedor.models import Fornecedor


# Create your models here.
    
class Categoria(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome 
    
class Produto(models.Model):
    nome = models.CharField(max_length=20)
    ncm = models.CharField(max_length=20)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT)
    preco = models.FloatField(blank=True)
    precovenda =  models.FloatField(blank=True)
    estoque = models.IntegerField(blank=True) #mudar pra quantidade
    estoquemin = models.IntegerField(blank=True)
    descricao = models.TextField(default='Sem descrição', null=True)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.nome 
    

