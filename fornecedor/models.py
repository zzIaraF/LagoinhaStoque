from django.db import models
from django.utils import timezone

# Create your models here.


class Fornecedor(models.Model):
    razaosocial = models.CharField(max_length=20)
    cnpj = models.IntegerField(blank=True)
    endereco = models.CharField(max_length=100)
    telefone = models.IntegerField()
    data = models.DateField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.razaosocial 
    
