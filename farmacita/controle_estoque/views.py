from django.shortcuts import render, redirect
from .models import lote_medicamento
from pessoas.models import fornecedor
from cadastro_medicamentos.models import medicamento
from pessoas.models import funcionario
from pessoas.views import failed_login

from django.http.response import HttpResponse
from datetime import timedelta
import xlwt
from django.db.models import Sum
from django.db.models.functions import (ExtractDay, ExtractMonth, ExtractQuarter, ExtractWeek,ExtractIsoWeekDay, ExtractWeekDay, ExtractIsoYear, ExtractYear)
from financeiro.models import ordem_de_venda
from django.db.models.fields import DecimalField, FloatField, IntegerField
from django.db.models import F, ExpressionWrapper
from datetime import date
from datetime import datetime

# Create your views here.

def checar_cargo(request):
    user = request.user
    if user.is_anonymous:
        return True, redirect('/')
    else:
        cargo = funcionario.objects.get(user=request.user).cargo
        if cargo == 'Caixa':
            return True, render(request,'sem_permissao.html',{'cargo':cargo})
    return False, False
    

def entrada_estoque(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    sucesso = False
    if request.method == "POST":
        p = request.POST
        print(p.get('nome_medicamento'))
        medicamento_usado = medicamento.objects.get(nome_medicamento=p.get('nome_medicamento'))
        fornecedor_usado = fornecedor.objects.get(nome_fornecedor=p.get('nome_fornecedor'))
        novo_lote = lote_medicamento(
            id_medicamento = medicamento_usado,
            id_fornecedor =  fornecedor_usado,
            preco = p.get('preco'),
            quantidade_de_caixas = p.get('quantidade_de_caixas'),
            quantidade_por_caixa = p.get('quantidade_por_caixa') + ' ' + p.get('unidade_quantidade_por_caixa'),
            dosagem = p.get('dosagem') + ' ' + p.get('unidade_dosagem'),
            data_de_validade = p.get('data_de_validade'),
            industria_farmaceutica = p.get('industria_farmaceutica'),
        )
    
        novo_lote.save()   
        sucesso = True

    nomes_medicamentos_validos = []
    medicamentos_validos=medicamento.objects.filter(excluido = False)
    for x in medicamentos_validos:
        nomes_medicamentos_validos.append(x.nome_medicamento)
    
    nomes_fornecedores_validos = []
    fornecedores_validos = fornecedor.objects.filter(ativo=True)
    for x in fornecedores_validos:
        nomes_fornecedores_validos.append(x.nome_fornecedor)


    return render(request,'estoque/pagina_de_entrada_de_estoque.html',{"nomes_medicamentos_validos":nomes_medicamentos_validos,"nomes_fornecedores_validos":nomes_fornecedores_validos,"sucesso":sucesso,'cargo':cargo})

def excluir_lote(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    sucesso=False
    if request.method == "POST":
        p = request.POST
        excluirlote = lote_medicamento.objects.get(id_medicamento=p.get('numero_lote'))
        excluirlote.excluido = True
        excluirlote.save()
        sucesso=True

    return render(request,'estoque/pagina_excluir_lote.html',{"sucesso":sucesso,'cargo':cargo})

def editar_lote(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    editar = False
    nomes_medicamentos_validos = []
    nomes_fornecedores_validos = []
    if request.user.is_authenticated:
        
        lista = lote_medicamento.objects.filter(excluido=False).order_by('data_de_validade')
        
        busca = request.GET.get('buscalote')
        if busca:
            lista = lote_medicamento.objects.filter(excluido=False,id_medicamento__in=medicamento.objects.filter(excluido=False,nome_medicamento__icontains = busca)).order_by('data_de_validade')

        delete = request.GET.get('delete')
        
        if delete:            
            teste = lote_medicamento.objects.filter(excluido=False,id_lote_medicamento = delete)
            teste.update(excluido= True)

        editando = request.GET.get('edit')
        if editando:
            editar = True
            lista = lote_medicamento.objects.filter(excluido=False,id_lote_medicamento = editando)
            medicamentos_validos=medicamento.objects.filter(excluido = False)
            for x in medicamentos_validos:
                nomes_medicamentos_validos.append(x.nome_medicamento)
            fornecedores_validos = fornecedor.objects.filter(ativo=True)
            for x in fornecedores_validos:
                nomes_fornecedores_validos.append(x.nome_fornecedor)

        if request.method == "POST":
            p = request.POST          
            medicamento_usado = medicamento.objects.get(nome_medicamento=p.get('nome_medicamento'))
            fornecedor_usado = fornecedor.objects.get(nome_fornecedor=p.get('nome_fornecedor'))
            editarlote = lote_medicamento.objects.filter(excluido=False,id_lote_medicamento = editando)

            validade = p.get('data_de_validade')

            if(validade == ""):
                validade = editarlote.first().data_de_validade

            editarlote.update(
                id_medicamento = medicamento_usado,
                id_fornecedor =  fornecedor_usado,
                preco = p.get('preco'),
                quantidade_de_caixas = p.get('quantidade_de_caixas'),
                quantidade_por_caixa = p.get('quantidade_por_caixa') + ' ' + p.get('unidade_quantidade_por_caixa'),
                dosagem = p.get('dosagem') + ' ' + p.get('unidade_dosagem'),
                data_de_validade = validade,
                industria_farmaceutica = p.get('industria_farmaceutica'),
            )
            
        return render(request,'estoque/pagina_edicao_lote.html',{'lista':lista,'cargo':cargo,'editar':editar,"nomes_medicamentos_validos":nomes_medicamentos_validos,"nomes_fornecedores_validos":nomes_fornecedores_validos})
    else:
        return failed_login(request)
    
    
    def gerar_relatorio_estoque(request):
     
    entrada  = lote_medicamento.objects. \
    select_related('id_medicamento').\
    values('id_medicamento__nome_medicamento'). \
    annotate(quant = Sum('quantidade_de_caixas', output_Field = FloatField())). \
    order_by('id_medicamento__nome_medicamento') \
   
    
    saida = ordem_de_venda.objects.filter(ativo=True,venda=True). \
    select_related('id_lote_medicamento', 'id_cliente').select_related('id_medicamento').\
    values('id_lote_medicamento__id_medicamento__nome_medicamento'). \
    annotate(quant = Sum('quantidade', output_Field = FloatField())). \
    order_by('id_lote_medicamento__id_medicamento__nome_medicamento')

    data_fin = datetime.now()
    data_ini = data_fin -  timedelta(days=30)

    comparativo = ordem_de_venda.objects.filter(ativo=True,venda=True,  data_de_venda__range = [data_ini, data_fin]). \
    select_related('id_lote_medicamento', 'id_cliente').select_related('id_medicamento').\
    values('id_lote_medicamento__id_medicamento__nome_medicamento'). \
    annotate(quant30 = Sum('quantidade', output_Field = FloatField()),
    valor = Sum('valor_total_venda', output_Field = FloatField())). \
    annotate(avg30 = ExpressionWrapper( F('valor')/F('quant30'), output_field=FloatField())). \
    order_by('id_lote_medicamento__id_medicamento__nome_medicamento')

   

    response = HttpResponse(content_type = 'application/vnd.ms-excel')

    dt = datetime.now()

    response['Content-Disposition'] = 'attachment; filename = Relatório para compras - ' +  str(date(dt.year, dt.month, dt.day)) + '.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Compras')
    row_num = 0

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    style.font = font
    style_string = "font: bold on; borders: bottom dashed"
    style = xlwt.easyxf(style_string)
    '''font_style = xlwt.XFStyle()
    font_style.font.bold = False
    '''
    columns = ['id_medicamento__nome_medicamento', 'quant', 'quant30', 'avg30']
    med = 'id_lote_medicamento__id_medicamento__nome_medicamento'

    ws.write(row_num,0, "Medicamento", style=style)
    ws.write(row_num,1, "Quantidade em estoque", style=style)
    ws.write(row_num,2, "Saída últimos 30 dias", style=style)
    ws.write(row_num,3, "Preço médio de venda últimos 30 dias", style=style)
 
    saida_row = 0
    comparativo_row = 0

    for row in entrada:
        row_num +=1

        ws.write(row_num, 0, row[columns[0]])

        if(row[columns[0]] == saida[saida_row][med]):
            
            ws.write(row_num, 1,  row[columns[1]] - saida[saida_row][columns[1]] )
            saida_row +=1
            if(row[columns[0]] == comparativo[comparativo_row][med]):
                ws.write(row_num, 2, comparativo[comparativo_row][columns[2]])
                ws.write(row_num, 3, comparativo[comparativo_row][columns[3]])
                comparativo_row +=1
            else:
                ws.write(row_num, 2, 0)
            
        else:
            ws.write(row_num, 1,  row[columns[1]])
            ws.write(row_num, 2, (0))
                
    wb.save(response)
    return response
