from django.urls import path
from . import views

urlpatterns = [
    path('entrada_estoque',views.entrada_estoque, name = 'entrada_estoque'),
    path('excluir_lote',views.excluir_lote, name = 'excluir_lote'),
    path('editar_lote',views.editar_lote, name = 'editar_lote'),
    path('gerar_relatorio_estoque',views.gerar_relatorio_estoque, name = 'gerar_relatorio_estoque')
]
