from django.db import models
from cadastro_medicamentos.models import medicamento
# Create your models here.

class lote_medicamento(models.Model):
    id_lote_medicamento = models.AutoField(primary_key=True)
    id_medicamento = models.ForeignKey(medicamento,on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=40,decimal_places=2)
    preco_com_desconto = models.DecimalField(max_digits=40,decimal_places=2)
    quantidade = models.IntegerField()
    quantidade_por_caixa = models.IntegerField()
    concentracao = models.CharField(max_length=100)
    formato = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    industria_farmaceutica = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    excluido = models.BooleanField(default=False)