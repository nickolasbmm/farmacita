from django.shortcuts import render, HttpResponse, redirect
from .models import medicamento,  principio_ativo2, rel_medicamento_principio_ativo2
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
    
def cadastro_medicamentos(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    sucesso=False
    principiosativos = principio_ativo2.objects.all()
    droga_list = list()
    for i in principiosativos:
        droga_list.append(i.nome_principio_ativo2)
    if request.method == "POST":
        p = request.POST
        princ_ativo = p.get("principio_ativo").split(";")
        princ_ativo = princ_ativo[1:]
        item = medicamento(
            nome_medicamento = p.get("name"),
            classificacao = p.get("classificacao"), 
            #principio_ativo =p.get("principio_ativo")
            )
        
        item.save()
        pa = principio_ativo2.objects.all()
        princ = []
        for i in pa:
            if i.nome_principio_ativo2 in princ_ativo:
                princ.append(i)
        print(princ)
        item.principio_ativo.set(princ)
        
        #item.principio_ativo.add(p.get("principio_ativo"))  
        sucesso=True


    return render(request,'medicamento/pagina_cadastro_medicamento.html',{"droga":droga_list,"sucesso":sucesso,'cargo':cargo })

def default_editar_medicamento():
    med = medicamento.objects.filter(excluido = False)
    lista = list()
    for item in med:
        princ = ""
        princ_list = list()
        principios = rel_medicamento_principio_ativo2.objects.filter(medicamento = item).order_by('princ_ativo')
    
        for i in principios:
            princ = princ + '\n'+ i.princ_ativo.nome_principio_ativo2 
            princ_list.append(i.princ_ativo.nome_principio_ativo2)

        princ = princ[1:]
        lista.append({"med": item, "princ": princ, "princ_list": princ_list})
    return lista


def editar_medicamento(request):      
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    sucesso=False
    

    lista = default_editar_medicamento

    editar = False
    
    busca = request.GET.get('buscamedic')

    if busca:
        editar = False
        lista = medicamento.objects.filter(nome_medicamento__icontains = busca)

    delete = request.GET.get('delete')
    
    if delete:            
        teste = medicamento.objects.filter(id_medicamento = delete)
        teste.update(excluido = True)
        lista = default_editar_medicamento
    
    editando = request.GET.get('edit')
    if editando:
        editar = True
        
        med = medicamento.objects.filter(id_medicamento = editando)

        lista = list()
        for item in med:
            princ = ""
            princ_list = list()
            principios = rel_medicamento_principio_ativo2.objects.filter(medicamento = item).order_by('princ_ativo')
        
            for i in principios:
                princ = princ + '\n'+ i.princ_ativo.nome_principio_ativo2 
                princ_list.append(i.princ_ativo.nome_principio_ativo2)

            princ = princ[1:]
            lista.append({"med": item, "princ": med, "princ_list": princ_list})

        

    principiosativos = principio_ativo2.objects.all()
    droga_list = list()
    for i in principiosativos:
        droga_list.append(i.nome_principio_ativo2)

   
    if request.method == "POST":
        p = request.POST

        princ_ativo = p.get("principio_ativo").split(";")
        princ_ativo = princ_ativo[1:]


        lista[0]["princ"].update(
            nome_medicamento = p.get("name"),
            classificacao = p.get("classificacao"), 
        )
        
        princ_ativo = p.get("principio_ativo").split(";")
        princ_ativo = princ_ativo[1:]
        rel_medicamento_principio_ativo2.objects.filter(medicamento =  lista[0]["med"]).delete()
        pa = principio_ativo2.objects.all()
        princ = []
        for i in pa:
            if i.nome_principio_ativo2 in princ_ativo:
                princ.append(i)
        
        lista[0]["med"].principio_ativo.set(princ)

        lista = default_editar_medicamento
        editar = False
        sucesso=True


    return render(request,'medicamento/editar_medicamento.html',
    {'lista':lista,
    'editar':editar,
    "droga":droga_list,
    "sucesso":sucesso,
    'cargo':cargo}
    )


def cadastrar_principio_ativo(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    if request.method == "POST":
        p = request.POST
        novonome = p.get("nome_principio_ativo")
        novoprincipioativo = principio_ativo2(nome_principio_ativo=novonome)
        novoprincipioativo.save()

    return HttpResponse(200)

