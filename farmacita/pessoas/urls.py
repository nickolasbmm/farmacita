from django.urls import path
from . import views

urlpatterns = [
    #path('cursos',views.show_courses, name = 'show_courses'),
    path('authentication',views.authentication, name = 'authentication'),
    path('principal',views.principal, name = 'principal'),
    path('cadastro_cliente',views.cadastro_cliente, name = 'cadastro_cliente'),
    path('cadastro_usuario',views.cadastro_usuario, name = 'cadastro_usuario'),
]