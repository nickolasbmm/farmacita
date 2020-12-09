from django.shortcuts import render
from .models import lote_medicamento
from pessoas.models import fornecedor
from cadastro_medicamentos.models import medicamento

# Create your views here.

def entrada_estoque(request):

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

    nomes_medicamentos_validos = []
    medicamentos_validos=medicamento.objects.all()
    for x in medicamentos_validos:
        nomes_medicamentos_validos.append(x.nome_medicamento)
    
    nomes_fornecedores_validos = []
    fornecedores_validos = fornecedor.objects.all()
    for x in fornecedores_validos:
        nomes_fornecedores_validos.append(x.nome_fornecedor)


    return render(request,'pagina_de_entrada_de_estoque.html',{"nomes_medicamentos_validos":nomes_medicamentos_validos,"nomes_fornecedores_validos":nomes_fornecedores_validos})