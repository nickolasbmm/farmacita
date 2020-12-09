from django.shortcuts import render
from django.shortcuts import render
from pessoas.models import cliente, fornecedor, funcionario
from controle_estoque.models import lote_medicamento
from cadastro_medicamentos.models import medicamento
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


def criar_ordem_de_venda(request, busca, id):
    get_aplicar_deconto = request.GET.get('aplicar_desconto')
    if get_aplicar_deconto:
        aplicar_desconto = True
    cpf_cliente_validos = []
    clientes_validos = cliente.objects.all()

    for x in clientes_validos:
        cpf_cliente_validos.append(x.cpf)
        
    nome_med_validos= []
    
    
    medicamentos = medicamento.objects.all()
    for x in medicamentos:
        nome_med_validos.append(x.nome_medicamento)

    nome_med = ""
    if request.method == "POST":
        p = request.POST
        id_lote = p.get("id_lote")
        id_med = lote_medicamento.objects.get(id_lote_medicamento = id_lote).id_medicamento
        nome_med = medicamentos.get(id_medicamento = id_med)
        qtd = p.get("quantidade")
        #if qtd > lote_medicamento.objects.filter(id_lote_medicamento = id_lote).quantidade:
            #return render(request,'pagina_falha_criar_ordem_de_venda.html')
        cpf = p.get("cpf")
        novaordemvenda = cliente(
            id_cliente = cliente.objects.filter(cpf = cpf).id_cliente, 
            id_lote_medicamento = id_lote,
            quantidade = qtd,
            desconto = autorizar_desconto(p.get("cod_desconto"))
            )
        novaordemvenda.save()  
         
    return render(request,'financeiro/pagina_criar_ordem_de_venda.html', {"aplicar_desconto": aplicar_desconto,
                                                                            "cpf_cliente_validos":cpf_cliente_validos, 
                                                                            "nome_med_validos" : nome_med_validos, 
                                                                            "id_lote": id_lote,
                                                                            "nome_med" :nome_med} )


def pesquisa_lote(request):
    lote_med_id = []
    nome = []
    lista_lote = lote_medicamento.objects.all()
    for x in lista_lote:
        lote_med_id.append(x.id_lote_medicamento)
        nome.append(x.id_lote_medicamento)
    
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
        
        return render(request,'financeiro/pagina_criar_ordem_de_venda.html', {"id_lote": id_lote, 
                                                                                "cpf_cliente_validos":cpf_cliente_validos,
                                                                                "nome":nome,
                                                                                "lote_med_id":lote_med_id})

    return render(request,'financeiro/pagina_pesquisa_lote.html', {"lista": lista,
                                                            "nome_med_validos" : nome_med_validos, 
                                                            "busca" :busca} )





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