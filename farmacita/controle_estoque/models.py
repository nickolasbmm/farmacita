from django.db import models
from cadastro_medicamentos.models import medicamento
from pessoas.models import fornecedor
# Create your models here.

class lote_medicamento(models.Model):
    id_lote_medicamento = models.AutoField(primary_key=True)
    id_medicamento = models.ForeignKey(medicamento,on_delete=models.PROTECT)
    id_fornecedor = models.ForeignKey(fornecedor,on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=40,decimal_places=2)
    quantidade_de_caixas = models.CharField(max_length=100)
    quantidade_por_caixa = models.CharField(max_length=100)
    dosagem = models.CharField(max_length=100)
    data_de_validade = models.DateTimeField(auto_now=False,auto_now_add=False,null=False)
    industria_farmaceutica = models.CharField(max_length=100)
    excluido = models.BooleanField(default=False)