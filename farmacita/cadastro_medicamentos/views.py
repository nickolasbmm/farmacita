from django.shortcuts import render, HttpResponse
from .models import medicamento, principio_ativo

# Create your views here.
def cadastro_medicamentos(request):
    principiosativos = principio_ativo.objects.all()
    droga_list = list()
    for i in principiosativos:
        droga_list.append(i.nome_principio_ativo)
    if request.method == "POST":
        p = request.POST
        item = medicamento(
            nome_medicamento = p.get("name"),
            classificacao = p.get("classificacao"), 
            principio_ativo =p.get("principio_ativo")
            )
        item.save()

    return render(request,'medicamento/pagina_cadastro_medicamento.html',{"droga":droga_list})

def editar_medicamento(request):      
  
    lista = medicamento.objects.all()
    editar = False
    
    busca = request.GET.get('buscamedic')

    if busca:
        editar = False
        lista = medicamento.objects.filter(nome_medicamento__icontains = busca)

    delete = request.GET.get('delete')
    
    if delete:            
        teste = medicamento.objects.filter(id_medicamento = delete)
        teste.update(excluido = True)
    
    editando = request.GET.get('edit')
    if editando:
        editar = True
        lista = medicamento.objects.filter(id_medicamento = editando)

    principiosativos = principio_ativo.objects.all()
    droga_list = list()
    for i in principiosativos:
        droga_list.append(i.nome_principio_ativo)

    if request.method == "POST":
        p = request.POST
        lista.update(
        nome_medicamento = p.get("name"),
        classificacao = p.get("classificacao"), 
        principio_ativo =p.get("principio_ativo")
        )


    return render(request,'medicamento/editar_medicamento.html',
    {'lista':lista,
    'editar':editar,
    "droga":droga_list}
    )

'''
def excluir_medicamento(request):   
    if request.method == "POST":
        id_medicamento = request.id_medicamento
        editarmedicamento = medicamento.objects.filter(id_medicamento = id_medicamento)
        editarmedicamento.update(
           excluido = True
        )
    return render(request,'medicamento/pagina_exclusao_medicamento.html')
'''

def cadastrar_principio_ativo(request):
    if request.method == "POST":
        p = request.POST
        novonome = p.get("nome_principio_ativo")
        novoprincipioativo = principio_ativo(nome_principio_ativo=novonome)
        novoprincipioativo.save()

    return HttpResponse(200)

