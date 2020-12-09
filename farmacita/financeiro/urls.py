from django.urls import path
from . import views

urlpatterns = [
    #path('cursos',views.show_courses, name = 'show_courses'),
    path('pesquisa_lote',views.pesquisa_lote, name = 'pesquisa_lote'),
    path('criar_ordem_de_venda',views.criar_ordem_de_venda, name = 'criar_ordem_de_venda'),
    path('desistir_compra',views.desistir_compra, name = 'desistir_compra'),
    path('vender_medicamento',views.vender_medicamento, name = 'vender_medicamento'),
    path('comprar_medicamento',views.comprar_medicamento, name = 'comprar_medicamento')
]
