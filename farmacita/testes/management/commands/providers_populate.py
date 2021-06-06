from django.core.management.base import BaseCommand, CommandError
from pessoas.models import fornecedor
from django.db import transaction
import factory
from factory.django import DjangoModelFactory

class ProviderFactory(DjangoModelFactory):
    class Meta:
        model = fornecedor

    nome_fornecedor = factory.Faker("company")
    cnpj = factory.Faker("cnpj", locale = "pt_br")
    telefone = factory.Faker("phone_number", locale = "pt_br")
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
                provider = ProviderFactory()
                print(provider)


