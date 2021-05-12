from django.contrib import admin
from .models import medicamento, principio_ativo, principio_ativo2, rel_medicamento_principio_ativo2

# Register your models here.

admin.site.register(medicamento)
admin.site.register(principio_ativo)
admin.site.register(principio_ativo2)
admin.site.register(rel_medicamento_principio_ativo2)