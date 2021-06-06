from django.core.management.base import BaseCommand, CommandError
from pessoas.models import cliente
from django.db import transaction
from faker import Faker
# factories.py
import factory
from factory.django import DjangoModelFactory

faker_factory = Faker('pt_BR')

# Defining a factory
class CostumerFactory(DjangoModelFactory):
    class Meta:
        model = cliente

    nome_cliente = factory.Faker("name", locale = "pt_br")
    cpf = factory.Faker("cpf", locale = "pt_br")
    telefone = factory.Faker("phone_number",locale = "pt_br")
    data_nascimento = factory.Faker("date", locale = "pt_br")
    ativo = factory.Faker("boolean", locale = "pt_br")


class Command(BaseCommand):
    help = 'Insere dados dummy ao banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('qnt', nargs='+', type=int)
    
    @transaction.atomic
    def handle(self, *args, **options):
        for qnt in options['qnt']:
            self.stdout.write("Creating new data...")
            for _ in range(qnt):
                costumer = CostumerFactory()
                print(costumer)


