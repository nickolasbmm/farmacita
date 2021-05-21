import json
from django.contrib import admin
from .models import medicamento, principio_ativo2, rel_medicamento_principio_ativo2
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import JSONWidget, ManyToManyWidget

# Register your models here.


class MedicamentoResource(resources.ModelResource):
    principio_ativo = fields.Field(attribute ='principio_ativo',
                                    widget=ManyToManyWidget(principio_ativo2, separator = ';', field = 'nome_principio_ativo2'))


    class Meta:
        model = medicamento
        import_id_fields = ('nome_medicamento',)
        fields = ['nome_medicamento',  'classificacao','principio_ativo']


class MedicamentoDataAdmin(ImportExportModelAdmin):
    resource_class = MedicamentoResource

admin.site.register(medicamento, MedicamentoDataAdmin)

class PrincipioAtivoResource(resources.ModelResource):
    
    class Meta:
        model = principio_ativo2
        import_id_fields = ('nome_principio_ativo2',)
        exclude = ['id_principio_ativo2']
        

class PrincipioAtivoDataAdmin(ImportExportModelAdmin):
    resource_class = PrincipioAtivoResource

admin.site.register(principio_ativo2, PrincipioAtivoDataAdmin)


admin.site.register(rel_medicamento_principio_ativo2)