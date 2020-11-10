from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

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