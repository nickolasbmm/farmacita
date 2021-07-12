from django.db.models.fields import DecimalField, FloatField, IntegerField
from django.db.models import F, ExpressionWrapper
from django.shortcuts import render, redirect
from django.shortcuts import render
from pessoas.models import cliente, fornecedor, funcionario
from controle_estoque.models import lote_medicamento
from cadastro_medicamentos.models import medicamento, rel_medicamento_principio_ativo2
from django.contrib.auth.models import User
from datetime import datetime
from .models import ordem_de_venda
import pandas as pd
import json
import decimal
from datetime import date
from django.db.models import F

from django.http.response import HttpResponse
from datetime import timedelta
import xlwt
from django.db.models import Sum

from django.db.models.functions import (ExtractDay, ExtractMonth, ExtractQuarter, ExtractWeek,ExtractIsoWeekDay, ExtractWeekDay, ExtractIsoYear, ExtractYear)

# Create your views here.

def checar_cargo(request):
    user = request.user
    if user.is_anonymous:
        return True, redirect('/')
    else:
        cargo = funcionario.objects.get(user=request.user).cargo
        if cargo == 'Farmacêutico':
            return True, render(request,'sem_permissao.html',{'cargo':cargo})
    return False, False

def cadastrar_ordem_de_venda(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo    
    datatable = json.loads(request.POST["datatable"])
    df = pd.DataFrame.from_dict(datatable)
    #print(df.columns)
    df.columns = [
        "nome", "quantidade", "dosagem", 
        "preco",
        "subtotal", "botao", "id_lote_medicamento"]
    df = df.astype({"preco" : float, "subtotal" : float, "quantidade" : int})
    #print(df)

    cpf = request.POST["cpf"]
    id_cliente = cliente.objects.get(cpf = cpf)
    desconto = request.POST["perc_desconto"] != ''
    percentual_desconto = 0

    if desconto:
        percentual_desconto = float(request.POST["perc_desconto"])

    for i, row in df.iterrows():
        #print("aqui a row:", row)
        ov = ordem_de_venda(
            id_cliente = id_cliente,
            id_lote_medicamento = lote_medicamento.objects.get(id_lote_medicamento = row["id_lote_medicamento"]),
            quantidade = row["quantidade"],
            desconto = desconto,
            venda = False,
            ativo = True,
            data_de_venda = date.today(),
            percentual_desconto = percentual_desconto,
            preco_desconto = row["preco"] * (1 - float(percentual_desconto)/100),
            valor_total_venda = row["preco"] * (1 - float(percentual_desconto)/100) * row["quantidade"]
        )
        ov.save()
        lote_medicamento.objects.filter(
            excluido=False,
            id_lote_medicamento=row["id_lote_medicamento"]
            ).update(quantidade_de_caixas = str(F('quantidade_de_caixas')- row["quantidade"]))

    return redirect("criar_ordem_de_venda")

def criar_ordem_de_venda(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo

    clientes_validos = cliente.objects.filter(ativo=True)
    cpf_cliente_validos = [x.cpf for x in clientes_validos]
    
    medicamentos = medicamento.objects.filter(excluido = False)
    med_validos = pd.DataFrame.from_records([{"id_medicamento_id":x.id_medicamento,"nome":x.nome_medicamento, "classificacao":x.classificacao} for x in medicamentos])
    lotes = pd.DataFrame.from_records(lote_medicamento.objects.filter(excluido = False).values())
    lotes = lotes.astype({"preco" : float, "quantidade_de_caixas" : str,"quantidade_por_caixa": str,  "data_de_validade" : str, "excluido": str})

    lotes = lotes.loc[(lotes["quantidade_de_caixas"] > str(0)) & (lotes["data_de_validade"] > str(date.today()))]

    #lotes = lotes.loc[(lotes["quantidade_de_caixas"] > 0)]
    lotes = lotes.merge(
        med_validos,
        how = "left",
        on = "id_medicamento_id"
    )

    lista_principio_ativos = list()
    for id in lotes["id_medicamento_id"].unique():
        princ = ""
        principios = rel_medicamento_principio_ativo2.objects.filter(medicamento = id).order_by('princ_ativo')
    
        for i in principios:
            princ = princ + ";" + i.princ_ativo.nome_principio_ativo2 
        princ = princ[1:]
        lista_principio_ativos.append({"med":id, "princ": princ})
    #print(lista_principio_ativos)


    lotes = lotes.sort_values("data_de_validade", ascending = False).groupby('id_medicamento_id').tail()
    #print(lotes)
    
    return render(request,'financeiro/pagina_criar_ordem_de_venda.html', {
                                                            "med_validos" : lotes["nome"].unique().tolist(), 
                                                            "cpf_cliente_validos":cpf_cliente_validos,
                                                            'cargo':cargo,
                                                            "lotes" : lotes.to_dict("records"),
                                                            "nome": lotes["nome"].tolist(),
                                                            'lista_principio_ativos': lista_principio_ativos
                                                            
                                                            } )




def consultar_ordem_de_venda(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    editar = False
    cpf_cliente_validos = []
    clientes_validos = cliente.objects.filter(ativo=True)
    for x in clientes_validos:
        cpf_cliente_validos.append(x.cpf)

    lista = []

    busca2 = request.GET.get("buscaCliente")
    id_cli = 0
    lista_cli = cliente.objects.filter(ativo=True,cpf = busca2)
    for x in lista_cli:
        id_cli = x.id_cliente
    #print(id_cli)
    if busca2:
        editar = False
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli,ativo = True)
        for x in lista_ordem_de_venda:
            lista.append(x)

    vender = request.GET.get('vend')
    if vender: 
        editar = False           
        teste = ordem_de_venda.objects.filter(ativo=True,id_ordem_de_venda = vender)
        teste.update(venda = True)
        teste.update(ativo = False)
        lista = []
        id_lote = teste.get().id_lote_medicamento.id_lote_medicamento
        qtd = teste.get().quantidade
        busca2 = teste.get().id_cliente.cpf
        id_cli = teste.get().id_cliente.id_cliente
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli,ativo = True)
        for x in lista_ordem_de_venda:
            lista.append(x)
    
    vender_tudo = request.GET.get('vender_tudo')
    if vender_tudo:
        editar = False        
        cid = cliente.objects.filter(ativo=True,cpf = vender_tudo).first()
        teste = ordem_de_venda.objects.filter(ativo=True,id_cliente = cid)
        teste.update(venda = True)
        teste.update(ativo = False)
        #lista = []
        #id_lote = teste.get().id_lote_medicamento.id_lote_medicamento
        #qtd = teste.get().quantidade
        #busca2 = teste.get().id_cliente.cpf
        #id_cli = teste.get().id_cliente.id_cliente
        #lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli).filter(ativo = True)
        #for x in lista_ordem_de_venda:
        #    lista.append(x)

    delete = request.GET.get('delete')
    if delete:
        editar = False            
        teste = ordem_de_venda.objects.filter(ativo=True,id_ordem_de_venda = delete)
        teste.update(ativo = False)
        lista = []
        id_lote = teste.get().id_lote_medicamento.id_lote_medicamento
        qtd = teste.get().quantidade
        editarlote = lote_medicamento.objects.get(id_lote_medicamento=id_lote)
        editarlote.quantidade_de_caixas = str(int(editarlote.quantidade_de_caixas) + int(qtd))
        editarlote.save()
        busca2 = teste.get().id_cliente.cpf
        id_cli = teste.get().id_cliente.id_cliente
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli,ativo = True)
        for x in lista_ordem_de_venda:
            lista.append(x)
        

    lista_edit = []
    editando = request.GET.get('edit')
    if editando:
        editar = True
        lista_ordem_de_venda = ordem_de_venda.objects.filter(ativo=True,id_ordem_de_venda = editar)
        for x in lista_ordem_de_venda:
            lista.append(x)
        
        lista_editar_ordem = ordem_de_venda.objects.filter(ativo=True,id_ordem_de_venda = editando)
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
        for med in medicamento.objects.filter(excluido=False,nome_medicamento__icontains=busca):
            lista.append({'lotes':lote_medicamento.objects.filter(excluido=False,id_medicamento = med.id_medicamento).order_by('data_de_validade'),'nome_med':med.nome_medicamento})

    id_lote2 = request.GET.get('vender','') 
    nome2 = ''
    if id_lote2:
        lista = lote_medicamento.objects.filter(excluido=False,id_lote_medicamento=id_lote2)
        nome2 = lista.get().id_medicamento
        quant_est = lista.get().quantidade_de_caixas
        id_lote = id_lote2

    if request.method == "POST":
        p = request.POST
        qtd = p.get("quantidade")
        CPF = p.get("cpf")
        editar_ordem_venda = ordem_de_venda.objects.filter(ativo=True,id_ordem_de_venda = editando)
        
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
                        preco_desconto = lote_medicamento.objects.get(id_lote_medicamento=id_lote).preco*(1-decimal.Decimal(p.get('perc_desconto'))/100),
                        valor_total_venda = lote_medicamento.objects.get(id_lote_medicamento=id_lote).preco*int(qtd),
                    )
        else:
            editar_ordem_venda.update(
                id_lote_medicamento = lote_medicamento.objects.get(id_lote_medicamento=id_lote),
                id_cliente = cliente.objects.get(cpf = CPF), 
                quantidade = qtd,
                desconto=False,
                percentual_desconto=decimal.Decimal(0),
                preco_desconto = lote_medicamento.objects.get(id_lote_medicamento=id_lote).preco,
                valor_total_venda = lote_medicamento.objects.get(id_lote_medicamento=id_lote).preco*int(qtd),
                )
        
        editarlote = lote_medicamento.objects.get(id_lote_medicamento=id_lote)
        editarlote.quantidade_de_caixas = str(int(editarlote.quantidade_de_caixas) - int(qtd))
        editarlote.save()
        editar = False
        id_cli = editar_ordem_venda.get().id_cliente.id_cliente
        lista_ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cli,ativo = True)
        for x in lista_ordem_de_venda:
            lista.append(x)

    '''
    print({"busca": busca,
                                                                                "busca2":busca2,
                                                                                "lista":lista,
                                                                                "cpf_cliente_validos":cpf_cliente_validos,
                                                                                "editar":editar,
                                                                                "lista_edit":lista_edit,
                                                                                'cargo':cargo})'''
    return render(request, 'financeiro/pagina_consultar_ordem_de_venda.html', {"busca": busca,
                                                                                "busca2":busca2,
                                                                                "lista":lista,
                                                                                "cpf_cliente_validos":cpf_cliente_validos,
                                                                                "editar":editar,
                                                                                "lista_edit":lista_edit,
                                                                                'cargo':cargo})


def vender(id_cliente):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cliente, ativo = True)
    for ordem in ordem_de_venda:
        lote_medicamento = lote_medicamento.objects.filter(excluido=False,id_lote_medicamento = ordem.id_lote_medicamento)
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
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    if request.method == "POST":
        p = request.POST
        cpf = p.get("cpf")
        id_lote_medicamento = p.get("id_lote_medicamento")
        id_cliente = cliente.objects.filter(ativo=True,cpf = cpf).id_cliente
        ordem_de_venda = ordem_de_venda.objects.filter(id_cliente = id_cliente, id_lote_medicamento =id_lote_medicamento , ativo = True)
        ordem_de_venda.ativo = False
        ##nao sei se é necessário
        dados= {
            "ativo": ordem_de_venda.ativo
        }
        dados = json.dumps(dados)
    return render(request,'desistir_compra_medicamento.html',{'cargo':cargo})

def vender_medicamento(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    if request.method == "POST":
        p = request.POST
        cpf = p.get("cpf")
        id_cliente = cliente.objects.filter(ativo=True,cpf = cpf).id_cliente
        vender(id_cliente)
    return render(request,'pagina_vender_medicamento.html',{'cargo':cargo})


def comprar_medicamento(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    if request.method == "POST":
        p = request.POST
        cnpj = p.get("cnpj")
        cod_desconto = p.get("cod_desconto")
        novaordemvenda = cliente(
            id_fornecedor = cliente.objects.filter(ativo=True,cnpj = cnpj).id_fornecedor, 
            id_medicamento = p.get("id_medicamento"),
            preco_lote = p.get("preco_lote"),
            quantidade_lotes =  p.get("quantidade_lotes")
            )
        novaordemvenda.save()        
    return render(request,'pagina_criar_ordem_de_venda.html',{'cargo':cargo})


def historico_vendas(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    lista = ordem_de_venda.objects.filter(ativo=True,venda=True)
    if request.method == "POST":
        p = request.POST
        cpf = p.get("cpf")
        id_cliente = cliente.objects.filter(ativo=True,cpf__icontains = cpf)
        lista = ordem_de_venda.objects.filter(ativo=True,venda=True,id_cliente__in=id_cliente)
    else:
        lista = ordem_de_venda.objects.filter(ativo=True,venda=True)
    
    return render(request, 'financeiro/pagina_historico_de_vendas.html', {"lista":lista,'cargo':cargo})


def gerar_relatorio(request):
 
    data_fin = datetime.now()
    data_ini = data_fin - timedelta(30)

    vendas = ordem_de_venda.objects.filter(ativo=True,venda=True,data_de_venda__range = [data_ini, data_fin]).select_related('id_lote_medicamento').select_related('id_medicamento').values('id_lote_medicamento__id_medicamento__nome_medicamento').annotate(quant = Sum('quantidade', output_Field = FloatField()), valor = Sum('valor_total_venda', output_Field = FloatField())).annotate( avg = ExpressionWrapper( F('valor')/F('quant'), output_field=FloatField())).order_by()
    

    response = HttpResponse(content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Expenses' + str(datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id_lote_medicamento__id_medicamento__nome_medicamento', 'quant', 'valor', 'avg']

    font_style = xlwt.XFStyle
    
    ws.write(row_num,0, "Medicamento")
    ws.write(row_num,1, "Quantidade")
    ws.write(row_num,2, "Valor")
    ws.write(row_num,3, "Preço médio")

    for row in vendas:
        row_num +=1

        for col_num in range(len(columns)):
          
            ws.write(row_num, col_num, str(row[columns[col_num]]))

    
    wb.save(response)
    return response

def gerar_relatorio_vendas(request):
 
    data_fin = datetime.now()
    data_ini = data_fin
    #data_ini = data_ini.replace(day=1)
    data_ini = data_fin - timedelta(days=90)
    delta = data_fin - data_ini
    #data_ini = data_fin - timedelta(30)
    #data_de_venda__range = [data_ini, data_fin] dentro de filter
    #idadeS = Sum(( F('id_cliente__data_nascimento')-datetime.now()).years*'quantidade'), output_Field = FloatField())). \
    # annotate( idade = ExpressionWrapper( F('idadeS')/F('quant'), output_field=FloatField())).
    # annotate(diaS = Sum((datetime.today()-F('data_de_venda'))*F('quantidade'),output_Field = FloatField())). \
    data_fin_ant = data_ini - timedelta(days=1)
    #data_ini_ant = data_ini.replace(month = data_ini.month-1)
    data_ini_ant = data_fin_ant - timedelta(days=90)
    delta_ant = data_fin_ant - data_ini_ant

    comparativo  = ordem_de_venda.objects.filter(ativo=True,venda=True, data_de_venda__range = [data_ini_ant, data_fin_ant]). \
    select_related('id_lote_medicamento').select_related('id_medicamento').\
    values('id_lote_medicamento__id_medicamento__nome_medicamento', \
    quant_ant = Sum('quantidade')).order_by('id_lote_medicamento__id_medicamento__nome_medicamento')

    
    vendas = ordem_de_venda.objects.filter(ativo=True,venda=True, data_de_venda__range = [data_ini, data_fin]). \
    select_related('id_lote_medicamento', 'id_cliente').select_related('id_medicamento').\
    values('id_lote_medicamento__id_medicamento__nome_medicamento', \
    aux1 = (datetime.now().year - ExtractYear('id_cliente__data_nascimento'))*F('quantidade')). \
    annotate(quant = Sum('quantidade', output_Field = FloatField()), \
    valor = Sum('valor_total_venda', output_Field = FloatField()), 
    aux2 = ExpressionWrapper(F('percentual_desconto')*F('quantidade'), output_field=FloatField()), 
    diaS = Sum(ExtractDay('data_de_venda')*F('quantidade'), output_Field = FloatField())). \
    annotate(descS = Sum('aux2')).\
    annotate(idadeS = Sum('aux1')).\
    annotate( avg = ExpressionWrapper( F('valor')/F('quant'), output_field=FloatField())). \
    annotate( desc = ExpressionWrapper( F('descS')/F('quant'), output_field=FloatField())). \
    annotate( dia = ExpressionWrapper( F('diaS')/F('quant'), output_field=FloatField())). \
    annotate( idade = ExpressionWrapper( F('idadeS')/F('quant'), output_field=FloatField())).order_by('id_lote_medicamento__id_medicamento__nome_medicamento')

    ultimo_dia = data_ini.replace(month = data_ini.month+1) - timedelta(days=1)

    if(datetime.now().day == ultimo_dia.day):
        tipo = "Final"
    else:
        tipo = "Parcial"
    
    mes = dict([("January" , "Janeiro"), ("February" , "Fevereiro"), ("March" , "Março"), ("April" , "Abril"), ("May" , "Maio"), ("June" , "Junho"), ("July" , "Julho"), ("August" , "Agosto"), ("September" , "Setembro"), ("October" , "Outubro"), ("November" , "Novembro"), ("December" , "Dezembro")])

    response = HttpResponse(content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Relatório de vendas - ' + mes[str(datetime.now().strftime("%B"))] + ' - ' + tipo + '.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Vendas')
    row_num = 0

    columns = ['id_lote_medicamento__id_medicamento__nome_medicamento', 'quant', 'valor', 'avg', 'desc', 'dia', 'idade']

    
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    style.font = font
    style_string = "font: bold on; borders: bottom dashed"
    style = xlwt.easyxf(style_string)
    
    ws.write(row_num,0, "Medicamento", style=style)
    ws.write(row_num,1, "Quantidade", style=style)
    ws.write(row_num,2, "Valor", style=style)
    ws.write(row_num,3, "Preço médio",  style=style)
    ws.write(row_num,4, "Desconto médio", style=style)
    ws.write(row_num,5, "Dia média", style=style)
    ws.write(row_num,6, "Idade média", style=style)
 #   ws.write(row_num,7, "Comparativo", style=style)

    for row in vendas:
        row_num +=1

        for col_num in range(len(columns)):
          
            ws.write(row_num, col_num, row[columns[col_num]])

#        ws.write(row_num, 7, row[columns[1]]/delta.days - comparativo[row_num-1]['quant_ant']/delta_ant.days)

    wb.save(response)
    return response




