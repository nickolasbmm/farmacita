from django.db import models

# Create your models here.

class medicamento(models.Model):
    id_medicamento = models.IntegerField(primary_key=True)
    nome_medicamento = models.CharField(max_length=100)
    principio_ativo = models.CharField(max_length=100)
    excluido = models.BooleanField(default=False)
