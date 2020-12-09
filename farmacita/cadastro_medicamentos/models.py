from django.db import models

# Create your models here.

class medicamento(models.Model):
    id_medicamento = models.AutoField(primary_key=True)
    nome_medicamento = models.CharField(max_length=100)
    classificacao = models.CharField(max_length=100, default='Sem tarja')
    principio_ativo = models.CharField(max_length=100)
    excluido = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome_medicamento


class principio_ativo(models.Model):
    nome_principio_ativo = models.CharField(max_length=100)