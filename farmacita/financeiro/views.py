from django.shortcuts import render
from django.shortcuts import render
from pessoas.models import cliente, fornecedor, funcionario
from controle_estoque.models import lote_medicamento
from cadastro_medicamentos.models import medicamento
from django.contrib.auth.models import User
from datetime import datetime
from .models import ordem_de_venda
import json

# Create your views here.
def autorizar_desconto(password):
    user = User.objects.filter(password = password)
    func = funcionario.objects.get(user=user).id
    if(func):
        return True
    return False



def criar_ordem_de_venda(request):
    quant_est = 0
    cpf_cliente_validos = []

    clientes_validos = cliente.objects.all()
    for x in clientes_validos:
        cpf_cliente_validos.append(x.cpf)
    
    medicamentos = medicamento.objects.all()
    nome_med_validos= []
    for x in medicamentos:
        nome_med_validos.append(x.nome_medicamento)
        
    
    lista = []
    busca = request.GET.get('buscaMedicamento')
    nome = busca
    if busca:
        id_med = medicamento.objects.get(nome_medicamento=busca).id_medicamento
        lista = lote_medicamento.objects.filter(id_medicamento = id_med).order_by('data_de_validade')
    
    id_lote = request.GET.get('vender') 
    
    if id_lote:
        lista = lote_medicamento.objects.filter(id_lote_medicamento=id_lote)
        busca = lista.get().id_medicamento
        quant_est = lista.get().quantidade_de_caixas 


    if request.method == "POST":
        p = request.POST
        qtd = p.get("quantidade")
        CPF = p.get("cpf")
        
        novaordemvenda = ordem_de_venda(
            id_lote_medicamento = lote_medicamento.objects.get(id_lote_medicamento=id_lote),
            id_cliente = cliente.objects.get(cpf = CPF), 
            quantidade = qtd,
            #desconto = autorizar_desconto(p.get("senha"))
            )
        novaordemvenda.save()
        

    return render(request,'financeiro/pagina_criar_ordem_de_venda.html', {"lista": lista,
                                                            "nome_med_validos" : nome_med_validos, 
                                                            "busca" :busca,
                                                            "id_lote": id_lote,
                                                            "nome": nome,
                                                            "quant_est": quant_est,
                                                            "cpf_cliente_validos":cpf_cliente_validos} )


def consultar_ordem_de_venda(request):
    cpf_cliente_validos = []
    clientes_validos = cliente.objects.all()
    for x in clientes_validos:
        cpf_cliente_validos.append(x.cpf)

    lista = []

    busca = request.GET.get("buscaCliente")
    id_cli = 0
    lista_cli = cliente.objects.filter(cpf = busca)
    for x in lista_cli:
        id_cli = x.id_cliente
    print(id_cli)
    if busca:
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli).filter(ativo = True)
        for x in lista_ordem_de_venda:
            lista.append(x)

    delete = request.GET.get('delete')
    if delete:            
            teste = ordem_de_venda.objects.filter(id_ordem_de_venda = delete)
            teste.update(ativo = False)

   


    return render(request, 'financeiro/pagina_consultar_ordem_de_venda.html', {"busca": busca,
                                                                                "lista":lista,
                                                                                "cpf_cliente_validos":cpf_cliente_validos})


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