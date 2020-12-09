from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_medicamentos',views.cadastro_medicamentos, name = 'cadastro_medicamentos'),
    path('editar_medicamento',views.editar_medicamento, name = 'editar_medicamento'),
    #path('excluir_medicamento',views.excluir_medicamento, name = 'excluir_medicamento'),
    path('cadastrar_principio_ativo',views.cadastrar_principio_ativo, name = 'cadastrar_principio_ativo')
]
