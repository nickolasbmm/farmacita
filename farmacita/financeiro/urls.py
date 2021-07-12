from django.urls import path
from . import views

urlpatterns = [
    path('criar_ordem_de_venda',views.criar_ordem_de_venda, name = 'criar_ordem_de_venda'),
    path('consultar_ordem_de_venda',views.consultar_ordem_de_venda, name = 'consultar_ordem_de_venda'),
    path('desistir_compra',views.desistir_compra, name = 'desistir_compra'),
    path('vender_medicamento',views.vender_medicamento, name = 'vender_medicamento'),
    path('comprar_medicamento',views.comprar_medicamento, name = 'comprar_medicamento'),
    path('historico_vendas',views.historico_vendas, name = 'historico_vendas'),
    path('cadastrar_ordem_de_venda', views.cadastrar_ordem_de_venda, name='cadastrar_ordem_de_venda'),
    path('gerar_relatorio', views.gerar_relatorio, name='gerar_relatorio'),
    path('gerar_relatorio_vendas', views.gerar_relatorio_vendas, name='gerar_relatorio_vendas')
]
