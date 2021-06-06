from django.core.management.base import BaseCommand, CommandError
from pessoas.models import cliente
from controle_estoque.models import lote_medicamento
from financeiro.models import ordem_de_venda
from django.db import transaction
from datetime import date, datetime, timedelta
import random

import factory
from factory.django import DjangoModelFactory


def get_random_cliente():
    return random.choice(cliente.objects.all())
class vendasFactory(DjangoModelFactory):
    class Meta:
        model = ordem_de_venda
    
    id_cliente = factory.LazyFunction(get_random_cliente)
    id_lote_medicamento = factory.LazyFunction(lambda: random.choice(lote_medicamento.objects.all()))
    quantidade = factory.Faker("pyint", min_value = 1, max_value = 50)
    desconto =  0
    venda =  True
    ativo = True
    data_de_venda = factory.Faker("date_between", start_date='-1y', end_date='today')
    percentual_desconto = 0
    preco_desconto = factory.lazy_attribute(lambda o: o.id_lote_medicamento.preco)
    valor_total_venda = factory.lazy_attribute(lambda o: o.preco_desconto * o.quantidade)


class Command(BaseCommand):
    help = 'Insere dados dummy ao banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('qnt', nargs='+', type=int)
    
    @transaction.atomic
    def handle(self, *args, **options):
        for qnt in options['qnt']:
            self.stdout.write("Creating new data...")
            for _ in range(qnt):
                venda = vendasFactory()
                ordem_de_venda.objects.filter(
                    id_ordem_de_venda=venda.id_ordem_de_venda
                    ).update(
                        data_de_venda = datetime.now() - timedelta(random.randint(0, 365))
                        )
                print(venda.id_ordem_de_venda)


