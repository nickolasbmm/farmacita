from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
'''
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email',)
'''
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('password1', 'password2','username', 'email',)

class funcionarioForm(forms.ModelForm):
    class Meta:
        model = funcionario
        fields = ('nome_funcionario','cpf', 'telefone', 'cargo',)
        