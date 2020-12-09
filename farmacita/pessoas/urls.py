from django.urls import path
from . import views

urlpatterns = [
    #path('cursos',views.show_courses, name = 'show_courses'),
    path('authentication',views.authentication, name = 'authentication'),
    path('principal',views.principal, name = 'principal'),
    path('cadastro_cliente',views.cadastro_cliente, name = 'cadastro_cliente'),
    path('editar_cliente',views.editar_cliente, name = 'editar_cliente'),
    path('cadastro_fornecedor',views.cadastro_fornecedor, name = 'cadastro_fornecedor'),
    path('cadastro_usuario',views.cadastro_usuario, name = 'cadastro_usuario'),
    path('editar_usuario',views.editar_usuario, name = 'editar_usuario'),
    path('editar_fornecedor',views.editar_fornecedor, name = 'editar_fornecedor'),
    #path('demitir_usuario',views.demitir_usuario, name = 'demitir_usuario'),
    path('deslogar',views.deslogar,name='deslogar')
]