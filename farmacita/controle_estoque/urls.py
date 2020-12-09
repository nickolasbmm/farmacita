from django.urls import path
from . import views

urlpatterns = [
    #path('cursos',views.show_courses, name = 'show_courses'),
    path('entrada_estoque',views.entrada_estoque, name = 'entrada_estoque'),
    path('excluir_lote',views.excluir_lote, name = 'excluir_lote')
]