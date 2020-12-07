from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#from six import python_2_unicode_compatible
# Create your models here.

class funcionario(models.Model):
    BALCONISTA = 'Balconista'
    CAIXA = 'Caixa'
    FARMACEUTICO = 'Farmcêutico'
    GERENTE_FINANCEIRO = 'Gerente Financeiro'
    TIPOS_CARGO = (
        (BALCONISTA, 'Balconista'),
        (CAIXA, 'Caixa'),
        (FARMACEUTICO, 'Farmcêutico'),
        (GERENTE_FINANCEIRO, 'Gerente Financeiro')
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_funcionario = models.CharField(max_length=300)
    cpf = models.CharField(max_length=11) 
    telefone = models.CharField(max_length=12)
    cargo = models.CharField(max_length=20,choices=TIPOS_CARGO)
    #privilegio = models.CharField(max_length=100, blank=True)
    data_de_admissao = models.DateTimeField(auto_now=False,auto_now_add=True)
    #data_de_demissao = models.DateTimeField(auto_now=False,auto_now_add=False, blank=True)


    def get_type(self):
            try:
                if self.user.profile.cargo == funcionario.BALCONISTA:
                    return 'Balconista'
                elif self.user.profile.cargo == funcionario.CAIXA:
                    return 'Caixa'
                elif self.user.profile.cargo == funcionario.FARMACEUTICO:
                    return 'Farmacêutico'
                elif self.user.profile.cargo == funcionario.GERENTE_FINANCEIRO:
                    return 'Gerente Financeiro'
            except:
                return ''

class cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome_cliente = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=12)
    nome_cliente = models.CharField(max_length=400)

class fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    nome_fornecedor = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)
    telefone = models.CharField(max_length=12)