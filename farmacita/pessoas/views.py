from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import funcionario, cliente, fornecedor
from django.contrib.auth.models import User
import json

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
            
    return render(request,'pessoas/pagina_cadastro_cliente.html',{"sucesso":sucesso})

def editar_cliente(request): 
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

        if request.method == "POST":
            p = request.POST          
            user = request.user
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

        return render(request,'pessoas/edicao_cliente.html',{'lista':lista,'editar':editar})
    else:
        return failed_login(request)

def cadastro_usuario(request):
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

    return render(request,'pessoas/pagina_cadastro_de_usuario.html',{'sucesso':sucesso})

def editar_usuario(request):    
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

        return render(request,'pessoas/pagina_edicao_de_usuario.html',{'lista':lista,'editar':editar,'sucesso':sucesso})
    else:
        return failed_login(request)

''' nao vai ser utilizada
def demitir_usuario(request):
    if request.method == "POST":
        p = request.POST
        usuario = User.objects.get(username=p.get('usuario'))
        excluirfuncionario = funcionario.objects.get(user=usuario,nome_funcionario=p.get('nome_funcionario'))
        excluirfuncionario.data_de_demissao=p.get('data_de_demissao')
        usuario.is_active = False
        usuario.save()
        excluirfuncionario.save()

    return render(request,'pessoas/pagina_demissao_de_usuario.html')
'''

def cadastro_fornecedor(request):
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
            
    return render(request,'pessoas/pagina_cadastro_fornecedor.html',{'sucesso':sucesso})


def editar_fornecedor(request):    
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

        return render(request,'pessoas/pagina_edicao_de_fornecedor.html',{'lista':lista,'editar':editar,'sucesso':sucesso})
    else:
        return failed_login(request)


    

