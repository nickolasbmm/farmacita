from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import funcionario, cliente, fornecedor

# Create your views here.

def principal(request):
    return render(request,'sucessful_login.html')

def authentication(request):
    if request.user.is_authenticated:
        return sucessful_login(request)
    elif request.method == 'POST':
        post = request.POST
        username = post.get('usuario', default=None)
        password = post.get('senha', default=None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return sucessful_login(request)
        else:
            return failed_login(request)
    else:
        return failed_login(request)

def sucessful_login(request):
    return redirect('principal')

def failed_login(request):
    return render(request,'login_page.html')

def cadCliente(request):
    valido = True
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("save"):
                p = request.POST
                
                item = cliente(nome_cliente = p.get("name"), cpf = p.get("cpf"), telefone =p.get("tel"))
                item.save()
                
        return render(request,'cliente/pagina_cadastro_cliente.html',{})
    else:
        return failed_login(request)

def editCliente(request):
    if request.user.is_authenticated:
        lista = cliente.objects.all()
        
        busca = request.GET.get('buscacliente')
        if busca:
            lista = cliente.objects.filter(nome_cliente__icontains = busca)
        
        
        if request.method == "POST":
            if request.POST.get("save"):
                p = request.POST
                
                item = cliente(nome_cliente = p.get("name"), cpf = p.get("cpf"), telefone =p.get("tel"))
                item.save()
                
        return render(request,'cliente/editar.html',{'lista':lista})
    else:
        return failed_login(request)


def cadUsuario(request):
    return render(request,'funcionario/pagina_cadastro_de_usuario.html',{})

def editFuncionario(request):
    lista = funcionario.objects.all()
    
    busca = request.GET.get('buscafunc')
    if busca:
        lista = funcionario.objects.filter(nome_funcionario__icontains = busca)
    
    
    if request.method == "POST":
        if request.POST.get("save"):
            p = request.POST
            
            item = cliente(nome_funcionario = p.get("name"), cpf = p.get("cpf"), telefone =p.get("tel"))
            item.save()
            
    return render(request,'funcionario/editar.html',{'lista':lista})


##### fazer busca de usuario



