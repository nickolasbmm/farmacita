from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import funcionario, cliente, fornecedor
from financeiro.models import ordem_de_venda
from controle_estoque.models import lote_medicamento
from cadastro_medicamentos.models import medicamento
from django.contrib.auth.models import User
from django.db.models import F
import json
import pandas as pd

# Create your views here.

def deslogar(request):
    logout(request)
    return redirect('/')

def pagina_principal(request):
    try:
        user = request.user
        func =  funcionario.objects.filter(user = user)[0]
        cargo = func.cargo
        return render(request,'pessoas/inicio.html', {'nome_funcionario':func.nome_funcionario,'cargo':cargo})
    except:
        return failed_login(request)

def authentication(request):
    if request.user.is_authenticated:
        return sucessful_login(request)
    elif request.method == 'POST':
        post = request.POST
        username = post.get('usuario', default=None)
        password = post.get('senha', default=None)
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return sucessful_login(request)
        else:
            return failed_login(request)
    else:
        return failed_login(request)

def sucessful_login(request):
    return redirect('pagina_principal')

def failed_login(request):
    return render(request,'login_page.html')

def cadastro_cliente(request): 
    cargo = funcionario.objects.get(user=request.user).cargo 
    sucesso=False 
    if request.method == "POST":
        p = request.POST
          
        novocliente = cliente(
            nome_cliente = p.get("name"), 
            cpf = p.get("cpf"), 
            telefone = p.get("tel"), 
            data_nascimento = p.get("data_nasc")
            )
        novocliente.save()
        sucesso=True
            
    return render(request,'pessoas/pagina_cadastro_cliente.html',{"sucesso":sucesso,'cargo':cargo})

def editar_cliente(request): 
    cargo = funcionario.objects.get(user=request.user).cargo
    sucesso = False
    if request.user.is_authenticated:
        editar = False

        lista = cliente.objects.all()
        
        busca = request.GET.get('buscacliente')
        if busca:
            editar = False
            lista = cliente.objects.filter(nome_cliente__icontains = busca)

        delete = request.GET.get('delete')
        
        if delete:            
            teste = cliente.objects.filter(id_cliente = delete)
            teste.update(ativo = False)
        
        editando = request.GET.get('edit')
        if editando:
            editar = True
            lista = cliente.objects.filter(id_cliente = editando)

        compras = request.GET.get('compras')
        if compras:
            return compras_cliente(request,compras)

        if request.method == "POST":
            p = request.POST          
            editarcliente = cliente.objects.filter(id_cliente=editando)
                                    
            nasc = p.get('data_nascimento')
            
            if(nasc== ""):
                nasc = editarcliente.first().data_nascimento
            
            editarcliente.update(
                nome_cliente = p.get('nome_cliente'),
                telefone = p.get('telefone'),
                data_nascimento = nasc,
                
            )
            sucesso=True      

        return render(request,'pessoas/edicao_cliente.html',{'lista':lista,'editar':editar,'sucesso':sucesso,'cargo':cargo})
    else:
        return failed_login(request)

def cadastro_usuario(request):
    cargo = funcionario.objects.get(user=request.user).cargo
    sucesso=False
    if request.method == "POST":
        p = request.POST
        novousuario = User.objects.create_user(username=p.get("usuario"),password=p.get("senha"))
        novousuario.save()
        novofuncionario = funcionario(
            user = novousuario,
            nome_funcionario = p.get('nome_funcionario'),
            cpf = p.get('cpf'),
            telefone = p.get('telefone'),
            cargo = p.get('cargo'),
            data_de_admissao = p.get('data_de_admissao'),
        )
        print(novofuncionario.data_de_admissao)
        novofuncionario.save()
        sucesso=True

    return render(request,'pessoas/pagina_cadastro_de_usuario.html',{'sucesso':sucesso,'cargo':cargo})

def editar_usuario(request):   
    cargo = funcionario.objects.get(user=request.user).cargo 
    sucesso=False
    if request.user.is_authenticated:
        editar = False

        lista = funcionario.objects.all()
        
        busca = request.GET.get('buscacliente')
        if busca:
            editar = False
            lista = funcionario.objects.filter(nome_funcionario__icontains = busca)

        delete = request.GET.get('delete')
        data = request.GET.get('data_de_demissao')
        if delete:
            print("olha aki")
            teste = funcionario.objects.filter(id = delete)
            print(data)
            teste.update(data_de_demissao = data)
        
        editando = request.GET.get('edit')
        if editando:
            editar = True
            lista = funcionario.objects.filter(id = editando)

        if request.method == "POST":
            p = request.POST          
            user = request.user
            editarfuncionario = funcionario.objects.filter(id=editando)
            senha_nova = p.get('senha',None)
            senha_antiga = p.get('senha_antiga')
            if senha_nova != None:
                if user.check_password(senha_antiga):
                    user.set_password(senha_nova)
                    user.save()
                        
            admissao = p.get('data_de_admissao')
            demissao = p.get('data_de_demissao')
            if(admissao== ""):
                admissao = editarfuncionario.first().data_de_admissao
            if(demissao== ""):
                demissao = editarfuncionario.first().data_de_demissao

            editarfuncionario.update(
                nome_funcionario = p.get('nome_funcionario'),
                telefone = p.get('telefone'),
                cargo = p.get('cargo'),
                data_de_admissao = admissao,
                data_de_demissao= demissao
            )
            sucesso=True

        return render(request,'pessoas/pagina_edicao_de_usuario.html',{'lista':lista,'editar':editar,'sucesso':sucesso,'cargo':cargo})
    else:
        return failed_login(request)


def cadastro_fornecedor(request):
    cargo = funcionario.objects.get(user=request.user).cargo
    sucesso=False
    if request.method == "POST":
        p = request.POST
          
        novofornecedor = fornecedor(
            nome_fornecedor = p.get("nome_fornecedor"), 
            cnpj = p.get("cnpj"), 
            telefone = p.get("telefone"), 
            )
        novofornecedor.save()
        sucesso=True
            
    return render(request,'pessoas/pagina_cadastro_fornecedor.html',{'sucesso':sucesso,'cargo':cargo})


def editar_fornecedor(request):
    cargo = funcionario.objects.get(user=request.user).cargo    
    sucesso=False
    if request.user.is_authenticated:
        editar = False

        lista = fornecedor.objects.filter(ativo=True)
        
        busca = request.GET.get('buscafornecedor')
        if busca:
            editar = False
            lista = fornecedor.objects.filter(nome_fornecedor__icontains = busca)

        delete = request.GET.get('delete')
        if delete:
            teste = fornecedor.objects.filter(id_fornecedor = delete)
            teste.update(ativo=False)
        
        editando = request.GET.get('edit')
        if editando:
            editar = True
            lista = fornecedor.objects.filter(id_fornecedor = editando)

        if request.method == "POST":
            p = request.POST          
            editarfornecedor = fornecedor.objects.filter(id_fornecedor=editando)

            editarfornecedor.update(
                nome_fornecedor= p.get('nome_fornecedor'),
                telefone = p.get('telefone'),
            )
            sucesso=True

        return render(request,'pessoas/pagina_edicao_de_fornecedor.html',{'lista':lista,'editar':editar,'sucesso':sucesso,'cargo':cargo})
    else:
        return failed_login(request)

def compras_cliente(request,id):
    cliente_selecionado = cliente.objects.get(id_cliente=id)
    cargo = funcionario.objects.get(user=request.user).cargo
    lista = ordem_de_venda.objects.filter(venda=True,id_cliente=cliente_selecionado)
    df = pd.DataFrame(list(lista.values()))
    df = df[['id_lote_medicamento_id','quantidade']]
    nomes = []
    for index,row in df.iterrows(): 
        nomes.append(lote_medicamento.objects.get(id_lote_medicamento=row['id_lote_medicamento_id']).id_medicamento.nome_medicamento)
    df['nome_medicamento'] = nomes
    df = df.groupby(['nome_medicamento'])['quantidade'].sum().reset_index()
    df = df.sort_values(['quantidade'], ascending=False)
    
    

    return render(request, 'pessoas/compras_cliente.html', {"lista":df.to_dict('records'),'cargo':cargo,'cliente':cliente_selecionado})


    

