from django.shortcuts import render, HttpResponse, redirect
from .models import medicamento,  principio_ativo2, rel_medicamento_principio_ativo2
from pessoas.models import funcionario
import pandas as pd

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
        
        princ_list = list()
        principios = rel_medicamento_principio_ativo2.objects.filter(medicamento = item).order_by('princ_ativo')
    
        for i in principios:
            princ_list.append(i.princ_ativo.nome_principio_ativo2)
        
        lista.append({"med": item, "princ": None, "princ_list": princ_list})
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
        lista = medicamento.objects.filter(excluido=False,nome_medicamento__icontains = busca)

    delete = request.GET.get('delete')
    
    if delete:            
        teste = medicamento.objects.filter(excluido=False,id_medicamento = delete)
        teste.update(excluido = True)
        lista = default_editar_medicamento
    
    editando = request.GET.get('edit')
    if editando:
        editar = True
        
        med = medicamento.objects.filter(excluido=False,id_medicamento = editando)

        lista = list()
        for item in med:
            princ_list = list()
            principios = rel_medicamento_principio_ativo2.objects.filter(medicamento = item).order_by('princ_ativo')
            for i in principios:
                princ_list.append(i.princ_ativo.nome_principio_ativo2)

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
        print("cadastrando")
        p = request.POST
        print(p.keys())
        novonome = p.get("nome_principio_ativo")
        novoprincipioativo = principio_ativo2(nome_principio_ativo2=novonome)
        novoprincipioativo.save()

    return HttpResponse(200)

def edicao_principio_ativo(request):
    check, retorno = checar_cargo(request)
    if check:
        return retorno
    cargo = funcionario.objects.get(user=request.user).cargo
    editar = False
    lista = []

    editando = request.GET.get('edit')
    if editando:
        editar = True
        lista = principio_ativo2.objects.filter(nome_principio_ativo2=editando)

    if request.method == "POST":
        p = request.POST
        if "newname" in list(p.keys()):
            newname = p.get("newname")
            p_ativo = principio_ativo2.objects.filter(nome_principio_ativo2=editando)
            p_ativo.update(nome_principio_ativo2 = newname)

        if "name2delete" in list(p.keys()):
            p2delete = p.get("name2delete")


            principio_ativo2.objects.filter(nome_principio_ativo2=p2delete).delete()

    p_ativos = principio_ativo2.objects.all()
    p_ativos = [p.nome_principio_ativo2 for p in p_ativos]
    p_ativos = pd.DataFrame(p_ativos, columns = ["Nome"])

    return render(
        request, 
        'medicamento/principio_ativo.html', 
        {
            "p_ativos" : p_ativos.to_html(
                table_id="p_ativos", classes="table table-hover", border = 0, index=False
            ),
            'editar':editar,
            'lista':lista,
        }
    )


