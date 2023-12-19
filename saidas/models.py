from django.db import models
from estoque.models import Produto
from django.utils import timezone

# Create your models here.

class Saidas(models.Model):
    data = models.DateField(default=timezone.now)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    
    def __str__(self):
        return f"Saida {self.id} - Produto: {self.produto.nome} - Data: {self.data}"
    
