from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_medicamentos',views.cadastro_medicamentos, name = 'cadastro_medicamentos')
]