from django.shortcuts import render
from django.shortcuts import render
from pessoas.models import cliente, fornecedor, funcionario
from django.contrib.auth.models import User
from datetime import datetime
import json

# Create your views here.
def autorizar_desconto(password):
    user = User.objects.filter(password = password)
    func = funcionario.objects.get(user=user)
    if(func.cargo == "Gerente Financeiro"):
        return True
    return False


def criar_ordem_de_venda(request):
    if request.method == "POST":
        p = request.POST
        id_lote = p.get("id_lote_medicamento")
        qtd = p.get("quantidade")
        if qtd > lote_medicamento.objects.filter(id_lote_medicamento = id_lote).quantidade:
            return render(request,'pagina_falha_criar_ordem_de_venda.html')
        cpf = p.get("cpf")
        novaordemvenda = cliente(
            id_cliente = cliente.objects.filter(cpf = cpf).id_cliente, 
            id_lote_medicamento = id_lote,
            quantidade = qtd,
            desconto = autorizar_desconto(p.get("cod_desconto"))
            )
        novaordemvenda.save()        
    return render(request,'pagina_criar_ordem_de_venda.html')


def vender(id_cliente):
    ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cliente, ativo = True)
    for ordem in ordem_de_venda:
        lote_medicamento = lote_medicamento.objects.filter(id_lote_medicamento = ordem.id_lote_medicamento)
        ordem.venda = True
        ordem.data_venda = datetime.now()
        ordem.ativo = False
        lote_medicamento.quantidade = lote_medicamento.quantidade-ordem.quantidade
        ##nao sei se é necessário
        dados= {
            "venda" : ordem.venda,
            "data_venda" : ordem.data_venda.isoformat(),
            "ativo": ordem.ativo,
            "quantidade" : lote_medicamento.quantidade
        }
        dados = json.dumps(dados)
        

def desistir_compra(request):
    if request.method == "POST":
        p = request.POST
        cpf = p.get("cpf")
        id_lote_medicamento = p.get("id_lote_medicamento")
        id_cliente = cliente.objects.filter(cpf = cpf).id_cliente
        ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cliente, id_lote_medicamento =id_lote_medicamento , ativo = True)
        ordem_de_venda.ativo = False
        ##nao sei se é necessário
        dados= {
            "ativo": ordem_de_venda.ativo
        }
        dados = json.dumps(dados)
    return render(request,'desistir_compra_medicamento.html')

def vender_medicamento(request):
    if request.method == "POST":
        p = request.POST
        cpf = p.get("cpf")
        id_cliente = cliente.objects.filter(cpf = cpf).id_cliente
        vender(id_cliente)
    return render(request,'pagina_vender_medicamento.html')


def comprar_medicamento(request):
    if request.method == "POST":
        p = request.POST
        cnpj = p.get("cnpj")
        cod_desconto = p.get("cod_desconto")
        novaordemvenda = cliente(
            id_fornecedor = cliente.objects.filter(cnpj = cnpj).id_fornecedor, 
            id_medicamento = p.get("id_medicamento"),
            preco_lote = p.get("preco_lote"),
            quantidade_lotes =  p.get("quantidade_lotes")
            )
        novaordemvenda.save()        
    return render(request,'pagina_criar_ordem_de_venda.html')
