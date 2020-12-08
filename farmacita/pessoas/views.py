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

def principal(request):
    return render(request,'sucessful_login.html')


##add fernanda
def direcionar_usuario(request,cargo):
        if cargo == "Balconista":
            print("você é balconista")
            return sucessful_login(request)
        elif cargo == "Caixa":
            print("você é caixa")
            return sucessful_login(request)
        elif cargo == "Farmacêutico":
            print("você é farmaceutico")
            return sucessful_login(request)
        elif cargo == "Gerente Financeiro":
            print("você é gerente financeiro")
            return sucessful_login(request)
        else:
            return failed_login(request)
##

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
            ##add fernanda
            return direcionar_usuario(request, user.cargo)
            ##
            return sucessful_login(request)
        else:
            return failed_login(request)
    else:
        return failed_login(request)

def sucessful_login(request):
    return redirect('principal')

def failed_login(request):
    return render(request,'login_page.html')

def cadastro_cliente(request):   
    if request.method == "POST":
        p = request.POST
          
        novocliente = cliente(
            nome_cliente = p.get("name"), 
            cpf = p.get("cpf"), 
            telefone = p.get("tel"), 
            data_nascimento = p.get("data_nasc")
            )
        novocliente.save()
            
    return render(request,'pagina_cadastro_cliente.html')

def cadastro_usuario(request):
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

    return render(request,'pagina_cadastro_de_usuario.html')


def editar_usuario(request):
    if request.method == "POST":
        p = request.POST
        user = request.user
        editarfuncionario = funcionario.objects.filter(user=user)
        senha_nova = p.get('senha',None)
        senha_antiga = p.get('senha_antiga')
        print(senha_nova)
        print(senha_antiga)
        print(user.password)
        if senha_nova != None:
            if user.check_password(senha_antiga):
                user.set_password(senha_nova)
                user.save()

        editarfuncionario.update(
            nome_funcionario = p.get('nome_funcionario'),
            cpf = p.get('cpf'),
            telefone = p.get('telefone'),
            cargo = p.get('cargo'),
            data_de_admissao = p.get('data_de_admissao'),
        )
        return redirect('/')

    user = funcionario.objects.get(user=request.user)
    dados= {
        "nome_funcionario" : user.nome_funcionario,
        "cpf" : user.cpf,
        "telefone" : user.telefone,
        "cargo" : user.cargo,
        "data_de_admissao" : user.data_de_admissao.isoformat()
    }
    dados = json.dumps(dados)
    
    return render(request,'pagina_edicao_de_usuario.html',{'dados':dados})


def demitir_usuario(request):
    if request.method == "POST":
        p = request.POST
        usuario = User.objects.get(username=p.get('usuario'))
        excluirfuncionario = funcionario.objects.get(user=usuario,nome_funcionario=p.get('nome_funcionario'))
        excluirfuncionario.data_de_demissao=p.get('data_de_demissao')
        usuario.is_active = False
        usuario.save()
        excluirfuncionario.save()

    return render(request,'pagina_demissao_de_usuario.html')

def cadastro_fornecedor(request):
    if request.method == "POST":
        p = request.POST
          
        novofornecedor = fornecedor(
            nome_fornecedor = p.get("nome_fornecedor"), 
            cnpj = p.get("cnpj"), 
            telefone = p.get("telefone"), 
            )
        novofornecedor.save()
            
    return render(request,'pagina_cadastro_fornecedor.html')


    

