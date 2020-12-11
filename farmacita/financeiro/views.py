from django.shortcuts import render
from django.shortcuts import render
from pessoas.models import cliente, fornecedor, funcionario
from controle_estoque.models import lote_medicamento
from cadastro_medicamentos.models import medicamento
from django.contrib.auth.models import User
from datetime import datetime
from .models import ordem_de_venda
import json
import decimal
# Create your views here.
# def autorizar_desconto(password):
#     user = User.objects.filter(password = password)
#     func = funcionario.objects.get(user=user).id
#     if(func):
#         return True
#     return False



def criar_ordem_de_venda(request):
    cargo = funcionario.objects.get(user=request.user).cargo
    sucesso = False
    
    quant_est = 0
    cpf_cliente_validos = []

    clientes_validos = cliente.objects.all()
    for x in clientes_validos:
        cpf_cliente_validos.append(x.cpf)
    
    medicamentos = medicamento.objects.all()
    med_validos= []
    for x in medicamentos:
        med_validos.append(x.nome_medicamento)
        
    
    lista = []
    busca = request.GET.get('buscaMedicamento','')
    nome = busca
    if busca:
        #busca=''
        for med in medicamento.objects.filter(nome_medicamento__icontains=busca):
            lista.append({'lotes':lote_medicamento.objects.filter(id_medicamento = med.id_medicamento).order_by('data_de_validade'),'nome_med':med.nome_medicamento})
    
    id_lote = request.GET.get('vender','') 
    nome2 = ''
    if id_lote:
        lista2 = lote_medicamento.objects.filter(id_lote_medicamento=id_lote)
        nome2 = lista2.get().id_medicamento
        quant_est = lista2.get().quantidade_de_caixas 
        cpf_cliente_validos = lista2.get().preco
        for med in medicamento.objects.filter(nome_medicamento=nome2):
            lista.append({'lotes':lista2,'nome_med':med.nome_medicamento})
    
        
        
    if request.method == "POST":
        p = request.POST
        qtd = p.get("quantidade")
        CPF = p.get("cpf")
        if p.get('desconto'):
            usuario = User.objects.get(username=p.get('login'))
            gerente = funcionario.objects.get(user=usuario)
            if usuario.check_password(p.get('senha')):
                if gerente.cargo == 'Gerente Financeiro' or gerente.cargo == 'Farmacêutico':
                    novaordemvenda = ordem_de_venda(
                        id_lote_medicamento = lote_medicamento.objects.get(id_lote_medicamento=id_lote),
                        id_cliente = cliente.objects.get(cpf = CPF), 
                        quantidade = qtd,
                        desconto=True,
                        percentual_desconto=decimal.Decimal(p.get('perc_desconto')),
                        preco_desconto = str(round(float(p.get("valor_total"))/int(qtd),2)),
                        valor_total_venda = p.get("valor_total")
                    )
                    editarlote = lote_medicamento.objects.get(id_lote_medicamento=id_lote)
                    editarlote.quantidade_de_caixas = str(int(editarlote.quantidade_de_caixas) - int(qtd))
                    editarlote.save()
                    novaordemvenda.save()
                else:
                    sucesso =False
                    
        else:
            print(p.get("valor_total"))
            novaordemvenda = ordem_de_venda(
                id_lote_medicamento = lote_medicamento.objects.get(id_lote_medicamento=id_lote),
                id_cliente = cliente.objects.get(cpf = CPF), 
                quantidade = qtd,
                preco_desconto = str(round(float(p.get("valor_total"))/int(qtd),2)),
                valor_total_venda = p.get("valor_total")
                )
            editarlote = lote_medicamento.objects.get(id_lote_medicamento=id_lote)
            editarlote.quantidade_de_caixas = str(int(editarlote.quantidade_de_caixas) - int(qtd))
            editarlote.save()
            novaordemvenda.save()

        
        sucesso=True
        

    return render(request,'financeiro/pagina_criar_ordem_de_venda.html', {"lista": lista,
                                                            "med_validos" : med_validos, 
                                                            "nome2" :nome2,
                                                            "id_lote": id_lote,
                                                            "nome": nome,
                                                            "quant_est": quant_est,
                                                            "cpf_cliente_validos":cpf_cliente_validos,
                                                            "sucesso":sucesso,
                                                            'cargo':cargo
                                                            } )




def consultar_ordem_de_venda(request):
    editar = False
    cargo = funcionario.objects.get(user=request.user).cargo
    cpf_cliente_validos = []
    clientes_validos = cliente.objects.all()
    for x in clientes_validos:
        cpf_cliente_validos.append(x.cpf)

    lista = []

    busca2 = request.GET.get("buscaCliente")
    id_cli = 0
    lista_cli = cliente.objects.filter(cpf = busca2)
    for x in lista_cli:
        id_cli = x.id_cliente
    print(id_cli)
    if busca2:
        editar = False
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli).filter(ativo = True)
        for x in lista_ordem_de_venda:
            lista.append(x)

    vender = request.GET.get('vend')
    if vender: 
        editar = False           
        teste = ordem_de_venda.objects.filter(id_ordem_de_venda = vender)
        teste.update(venda = True)
        teste.update(ativo = False)
        lista = []
        id_lote = teste.get().id_lote_medicamento.id_lote_medicamento
        qtd = teste.get().quantidade
        busca2 = teste.get().id_cliente.cpf
        id_cli = teste.get().id_cliente.id_cliente
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli).filter(ativo = True)
        for x in lista_ordem_de_venda:
            lista.append(x)


    delete = request.GET.get('delete')
    if delete:
        editar = False            
        teste = ordem_de_venda.objects.filter(id_ordem_de_venda = delete)
        teste.update(ativo = False)
        lista = []
        id_lote = teste.get().id_lote_medicamento.id_lote_medicamento
        qtd = teste.get().quantidade
        editarlote = lote_medicamento.objects.get(id_lote_medicamento=id_lote)
        editarlote.quantidade_de_caixas = str(int(editarlote.quantidade_de_caixas) + int(qtd))
        editarlote.save()
        busca2 = teste.get().id_cliente.cpf
        id_cli = teste.get().id_cliente.id_cliente
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli).filter(ativo = True)
        for x in lista_ordem_de_venda:
            lista.append(x)
        

    lista_edit = []
    editando = request.GET.get('edit')
    if editando:
        editar = True
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_ordem_de_venda = editar)
        for x in lista_ordem_de_venda:
            lista.append(x)
        
        lista_editar_ordem = ordem_de_venda.objects.filter(id_ordem_de_venda = editando)
        id_lote = lista_editar_ordem.get().id_lote_medicamento.id_lote_medicamento
        for x in lista_editar_ordem:
            lista_edit.append(x)
        
        qtd = lista_editar_ordem.get().quantidade
        editarlote = lote_medicamento.objects.get(id_lote_medicamento=id_lote)
        editarlote.quantidade_de_caixas = str(int(editarlote.quantidade_de_caixas) + int(qtd))
        editarlote.save()

    busca = request.GET.get('buscaMedicamento','')
    nome = busca
    if busca:
        #busca=''
        for med in medicamento.objects.filter(nome_medicamento__icontains=busca):
            lista.append({'lotes':lote_medicamento.objects.filter(id_medicamento = med.id_medicamento).order_by('data_de_validade'),'nome_med':med.nome_medicamento})

    id_lote2 = request.GET.get('vender','') 
    nome2 = ''
    if id_lote2:
        lista = lote_medicamento.objects.filter(id_lote_medicamento=id_lote2)
        nome2 = lista.get().id_medicamento
        quant_est = lista.get().quantidade_de_caixas
        id_lote = id_lote2

    if request.method == "POST":
        p = request.POST
        qtd = p.get("quantidade")
        CPF = p.get("cpf")
        editar_ordem_venda = ordem_de_venda.objects.filter(id_ordem_de_venda = editando)
        
        if p.get('desconto'):
            usuario = User.objects.get(username=p.get('login'))
            gerente = funcionario.objects.get(user=usuario)
            if usuario.check_password(p.get('senha')):
                if gerente.cargo == 'Gerente Financeiro' or gerente.cargo == 'Farmacêutico':
                    
                    editar_ordem_venda.update(
                        id_lote_medicamento = lote_medicamento.objects.get(id_lote_medicamento=id_lote),
                        id_cliente = cliente.objects.get(cpf = CPF), 
                        quantidade = qtd,
                        desconto=True,
                        percentual_desconto=decimal.Decimal(p.get('perc_desconto')),
                        preco_desconto = lote_medicamento.objects.get(id_lote_medicamento=id_lote).preco*(1-decimal.Decimal(p.get('perc_desconto'))/100)
                    )
        else:
            editar_ordem_venda.update(
                id_lote_medicamento = lote_medicamento.objects.get(id_lote_medicamento=id_lote),
                id_cliente = cliente.objects.get(cpf = CPF), 
                quantidade = qtd,
                desconto=False,
                percentual_desconto=decimal.Decimal(0),
                preco_desconto = lote_medicamento.objects.get(id_lote_medicamento=id_lote).preco
                )
        
        editarlote = lote_medicamento.objects.get(id_lote_medicamento=id_lote)
        editarlote.quantidade_de_caixas = str(int(editarlote.quantidade_de_caixas) - int(qtd))
        editarlote.save()
        editar = False
        id_cli = editar_ordem_venda.get().id_cliente.id_cliente
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli).filter(ativo = True)
        for x in lista_ordem_de_venda:
            lista.append(x)


    
    return render(request, 'financeiro/pagina_consultar_ordem_de_venda.html', {"busca": busca,
                                                                                "busca2":busca2,
                                                                                "lista":lista,
                                                                                "cpf_cliente_validos":cpf_cliente_validos,
                                                                                "editar":editar,
                                                                                "lista_edit":lista_edit,
                                                                                'cargo':cargo})


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
    cargo = funcionario.objects.get(user=request.user).cargo
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
    return render(request,'desistir_compra_medicamento.html',{'cargo':cargo})

def vender_medicamento(request):
    cargo = funcionario.objects.get(user=request.user).cargo
    if request.method == "POST":
        p = request.POST
        cpf = p.get("cpf")
        id_cliente = cliente.objects.filter(cpf = cpf).id_cliente
        vender(id_cliente)
    return render(request,'pagina_vender_medicamento.html',{'cargo':cargo})


def comprar_medicamento(request):
    cargo = funcionario.objects.get(user=request.user).cargo
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
    return render(request,'pagina_criar_ordem_de_venda.html',{'cargo':cargo})


def historico_vendas(request):
    cargo = funcionario.objects.get(user=request.user).cargo
    lista = ordem_de_venda.objects.filter(venda=True)


    
    return render(request, 'financeiro/pagina_historico_de_vendas.html', {"lista":lista,'cargo':cargo})
