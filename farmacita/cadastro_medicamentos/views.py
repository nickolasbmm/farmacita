from django.shortcuts import render, HttpResponse
from .models import medicamento, principio_ativo

# Create your views here.
def cadastro_medicamentos(request):
    droga = medicamento.objects.values_list("principio_ativo", flat=True)
    droga_list = list()
    for i in droga:
        droga_list.append(i)
    if request.method == "POST":
        p = request.POST
        item = medicamento(
            nome_medicamento = p.get("name"),
            classificacao = p.get("classificacao"), 
            principio_ativo =p.get("principio_ativo")
            )
        item.save()
        print(item.nome_medicamento)
    
    

    return render(request,'medicamento/pagina_cadastro_medicamento.html',{"droga":droga_list})

def editar_medicamento(request):   
    '''if request.method == "POST":
        p = request.POST
        id_medicamento = request.id_medicamento
        editarmedicamento = medicamento.objects.filter(id_medicamento = id_medicamento)
        editarmedicamento.update(
            nome_medicamento = p.get("name"),
            classificacao = p.get("classificacao"), 
            principio_ativo =p.get("principio_ativo")
        )'''
  
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


    return render(request,'medicamento/editar_medicamento.html',{'lista':lista,'editar':editar})

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

