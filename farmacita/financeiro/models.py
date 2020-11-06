from django.db import models
from pessoas.models import cliente
from controle_estoque.models import lote_medicamento

# Create your models here.

class ordem_de_venda(models.Model):
    id_ordem_de_venda = models.IntegerField(primary_key=True)
    id_cliente = models.ForeignKey(cliente,on_delete=models.PROTECT)
    id_lote_medicamento = models.ForeignKey(lote_medicamento,on_delete=models.PROTECT)
    desconto = models.DecimalField(max_digits=40,decimal_places=2)
