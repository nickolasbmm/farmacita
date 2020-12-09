from django.contrib import admin

from .models import ordem_de_venda

# Register your models here.

admin.site.register(ordem_de_venda)
admin.site.register(ordem_de_compra)
