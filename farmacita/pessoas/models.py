from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class funcionario:
    id_funcionario = models.ForeignKey(User,on_delete=models.PROTECT)
    nome_funcionario = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11) 
    telefone = models.IntegerField(max_length=12)
    cargo = models.CharField(max_length=100)
    privilegio = models.CharField(max_length=100)
    data_de_admissao = models.CharField(max_length=100)
    data_de_demissao = models.CharField(max_length=100)

class cliente:
    id_cliente = models.IntegerField(primary_key=True)
    nome_cliente = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.IntegerField(max_length=12)
    nome_cliente = models.CharField(max_length=400)

class fornecedor:
    id_fornecedor = models.IntegerField(primary_key=True)
    nome_fornecedor = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)
    telefone = models.IntegerField(max_length=12)