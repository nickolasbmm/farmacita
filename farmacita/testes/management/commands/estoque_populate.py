from django.core.management.base import BaseCommand, CommandError
from pessoas.models import fornecedor
from cadastro_medicamentos.models import medicamento
from controle_estoque.models import lote_medicamento
from django.db import transaction
import factory
from factory.django import DjangoModelFactory

class LoteFactory(DjangoModelFactory):
    class Meta:
        model = lote_medicamento

    id_medicamento = factory.Iterator(medicamento.objects.all())
    id_fornecedor = factory.Iterator(fornecedor.objects.all())
    preco = factory.Faker("pyfloat", right_digits = 2, positive = True, max_value = 1000)
    quantidade_de_caixas = factory.Faker("pyint")
    quantidade_por_caixa = factory.Faker("pyint")
    dosagem = factory.Faker("pyint")
    data_de_validade = factory.Faker("date_between", start_date='today', end_date='+30y')
    industria_farmaceutica = factory.Faker("company")
    excluido = factory.Faker("boolean")

class Command(BaseCommand):
    help = 'Insere dados dummy ao banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('qnt', nargs='+', type=int)
    
    @transaction.atomic
    def handle(self, *args, **options):
        for qnt in options['qnt']:
            self.stdout.write("Creating new data...")
            for _ in range(qnt):
                lote = LoteFactory()
                print(lote)


