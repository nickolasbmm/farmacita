from django.contrib import admin

from .models import funcionario, cliente, fornecedor

# Register your models here.

admin.site.register(funcionario)
admin.site.register(cliente)
admin.site.register(fornecedor)
