from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    #path('cursos',views.show_courses, name = 'show_courses'),
    path('register', views.register, name='register'),
    #path('update_funcionario',views.update_funcionario, name = 'update_funcionario'),
    #path('authentication',views.authentication, name = 'authentication'),
    path('principal',views.principal, name = 'principal'),
]