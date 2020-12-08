from django.urls import path
from . import views

urlpatterns = [
    #path('cursos',views.show_courses, name = 'show_courses'),
    path('authentication',views.authentication, name = 'authentication'),
    path('principal',views.principal, name = 'principal'),
    path('cadcliente',views.cadCliente, name = 'cadcliente'),
    path('editcliente',views.editCliente, name = 'editcliente'),
    path('cadusuario',views.cadUsuario, name = 'cadusuario'),
    path('editfunc',views.editFuncionario, name = 'editfunc'),     
]