from django.db import models
from pessoas.models import cliente
from controle_estoque.models import lote_medicamento
from cadastro_medicamentos.models import medicamento
from pessoas.models import fornecedor
from datetime import datetime
from cadastro_medicamentos.models import medicamento
from pessoas.models import fornecedor

# Create your models here.
'''
class ordem_de_venda(models.Model):
    id_ordem_de_venda = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(cliente,on_delete=models.PROTECT)
    id_lote_medicamento = models.ForeignKey(lote_medicamento,on_delete=models.PROTECT)
    desconto = models.DecimalField(max_digits=40,decimal_places=2)
'''

class ordem_de_venda(models.Model):
    id_ordem_de_venda = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(cliente,on_delete=models.PROTECT)
    id_lote_medicamento = models.ForeignKey(lote_medicamento,on_delete=models.PROTECT)
    quantidade = models.IntegerField(default = 0)
    desconto =  models.BooleanField(default=False)
    venda =  models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    data_de_venda = models.DateTimeField(auto_now=False,auto_now_add=False,null=True)

class ordem_de_compra(models.Model):
    id_ordem_de_compra = models.AutoField(primary_key=True)
    id_fornecedor = models.ForeignKey(fornecedor,on_delete=models.PROTECT)
    id_medicamento = models.ForeignKey(medicamento,on_delete=models.PROTECT)
    preco_lote = models.DecimalField(max_digits=40,decimal_places=2)
    quantidade_lote = models.IntegerField(default = 0)
    data_de_compra = models.DateTimeField(auto_now=True,auto_now_add=False, null=False)
    
