from django.shortcuts import render, redirect
from .models import lote_medicamento
from pessoas.models import fornecedor
from cadastro_medicamentos.models import medicamento
from pessoas.models import funcionario

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
    medicamentos_validos=medicamento.objects.all()
    for x in medicamentos_validos:
        nomes_medicamentos_validos.append(x.nome_medicamento)
    
    nomes_fornecedores_validos = []
    fornecedores_validos = fornecedor.objects.all()
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
    if request.user.is_authenticated:
        lista = lote_medicamento.objects.all().order_by('data_de_validade')
        
        busca = request.GET.get('buscalote')
        if busca:
            lista = lote_medicamento.objects.filter(id_medicamento__in=medicamento.objects.filter(nome_medicamento__icontains = busca)).order_by('data_de_validade')

        delete = request.GET.get('delete')
        
        if delete:            
            teste = lote_medicamento.objects.filter(id_lote_medicamento = delete)
            teste.update(excluido= True)
            
        return render(request,'estoque/pagina_edicao_lote.html',{'lista':lista,'cargo':cargo})
    else:
        return failed_login(request)