from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



# Create your models here.

# Para a lista de propriedades e métodos de User veja https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#user-model

class funcionario(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nome_funcionario = models.CharField(max_length=300)
    cpf = models.CharField(max_length=14) 
    telefone = models.CharField(max_length=15)
    cargo = models.CharField(max_length=100)
    #privilegio = models.CharField(max_length=100)
    data_de_admissao = models.DateTimeField(auto_now=False,auto_now_add=False,null=False)
    data_de_demissao = models.DateTimeField(auto_now=False,auto_now_add=False,null=True)
    class Meta:
        db_table = 'funcionarios'

class cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome_cliente = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField(default=datetime.now)
    ativo = models.BooleanField(default=True)
    class Meta:
        db_table = 'clientes'
    

class fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    nome_fornecedor = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=15)
