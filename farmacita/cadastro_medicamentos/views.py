from django.shortcuts import render, HttpResponse
from .models import medicamento, principio_ativo
from pessoas.models import funcionario

# Create your views here.
def cadastro_medicamentos(request):
    cargo = funcionario.objects.get(user=request.user).cargo
    sucesso=False
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
        sucesso=True

    return render(request,'medicamento/pagina_cadastro_medicamento.html',{"droga":droga_list,"sucesso":sucesso,'cargo':cargo})

def editar_medicamento(request):      
    sucesso=False
    cargo = funcionario.objects.get(user=request.user).cargo
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
        sucesso=True


    return render(request,'medicamento/editar_medicamento.html',
    {'lista':lista,
    'editar':editar,
    "droga":droga_list,
    "sucesso":sucesso,
    'cargo':cargo}
    )


def cadastrar_principio_ativo(request):
    if request.method == "POST":
        p = request.POST
        novonome = p.get("nome_principio_ativo")
        novoprincipioativo = principio_ativo(nome_principio_ativo=novonome)
        novoprincipioativo.save()

    return HttpResponse(200)

