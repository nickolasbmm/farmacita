from django.contrib import admin
from .models import medicamento, principio_ativo

# Register your models here.

admin.site.register(medicamento)
admin.site.register(principio_ativo)