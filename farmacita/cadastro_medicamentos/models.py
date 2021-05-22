from django.db import models

# Create your models here.

class principio_ativo2(models.Model):
    id_principio_ativo2 = models.AutoField(primary_key=True)
    nome_principio_ativo2 = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome_principio_ativo2

class medicamento(models.Model):
    id_medicamento = models.AutoField(primary_key=True)
    nome_medicamento = models.CharField(max_length=100)
    classificacao = models.CharField(max_length=100, default='Sem tarja')
    principio_ativo = models.ManyToManyField(principio_ativo2, through='rel_medicamento_principio_ativo2')
    excluido = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome_medicamento

class rel_medicamento_principio_ativo2(models.Model):
    medicamento = models.ForeignKey(medicamento,on_delete=models.PROTECT)
    princ_ativo = models.ForeignKey(principio_ativo2,on_delete=models.PROTECT)


