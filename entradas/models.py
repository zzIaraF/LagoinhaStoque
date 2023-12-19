from django.db import models
from estoque.models import Produto
from django.utils import timezone

# Create your models here.

class Entradas(models.Model):
    data = models.DateField(default=timezone.now)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    
    def __str__(self):
        return f"Entrada {self.id} - Produto: {self.produto.nome} - Data: {self.data}"
    