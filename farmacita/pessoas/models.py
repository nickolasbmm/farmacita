from django.db import models
from django.contrib.auth.models import User



# Create your models here.

# Para a lista de propriedades e métodos de User veja https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#user-model

class funcionario(User):
    id_funcionario = User.pk
    nome_funcionario = models.CharField(max_length=300)
    cpf = models.CharField(max_length=11) 
    telefone = models.CharField(max_length=12)
    cargo = models.CharField(max_length=100)
    privilegio = models.CharField(max_length=100)
    data_de_admissao = models.DateTimeField(auto_now=False,auto_now_add=True)
    data_de_demissao = models.DateTimeField(auto_now=False,auto_now_add=False)

class cliente(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    nome_cliente = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=12)
    

class fornecedor(models.Model):
    id_fornecedor = models.IntegerField(primary_key=True)
    nome_fornecedor = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)
    telefone = models.CharField(max_length=12)