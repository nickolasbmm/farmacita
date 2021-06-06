from django.core.management.base import BaseCommand, CommandError
from cadastro_medicamentos.models import medicamento, principio_ativo2
from django.db import transaction
import factory
from factory.django import DjangoModelFactory
import pandas as pd
df = pd.read_csv("../med_name_princ.csv")


# class MedicineFactory(DjangoModelFactory):
#     class Meta:
#         model = medicamento

#     nome_medicamento = models.CharField(max_length=100)
#     classificacao = models.CharField(max_length=100, default='Sem tarja')
#     principio_ativo = models.ManyToManyField(principio_ativo2, through='rel_medicamento_principio_ativo2')
#     excluido = models.BooleanField(default=False)


class Command(BaseCommand):
    help = 'Insere dados dummy ao banco de dados'
    
    @transaction.atomic
    def handle(self, *args, **options):
        for princs in df["ActiveIngredient"].tolist():
            for princ in str(princs).split("; "):
                principio_ativo2.objects.update_or_create(nome_principio_ativo2=princ)
        for i, row in df.iterrows():
            if i > 100:
                break
            med = row['DrugName']
            princs = row['ActiveIngredient']
            med_obj = medicamento(
                nome_medicamento = med,
                classificacao = "Sem tarja",
                excluido = False
            )
            med_obj.save()
            ps = principio_ativo2.objects.filter(nome_principio_ativo2__in=str(princs).split("; "))
            med_obj.principio_ativo.add(*[x.id_principio_ativo2 for x in ps])


