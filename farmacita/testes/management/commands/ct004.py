from django.core.management.base import BaseCommand, CommandError
from pessoas.models import cliente
from .functions import string_generate, testar_igualdade
import string

class Command(BaseCommand):
    help = 'Testa o caso teste CT-004 inserção de clientes no banco de dados'

    def handle(self, *args, **options):
        for i in range(10):
            insere = cliente(
                nome_cliente= string_generate(size = 100),
                cpf = string_generate(size = 11, chars= string.digits),
                telefone = string_generate(size = 12, chars= string.digits)
            )

            try:
                insere.save()
                user = cliente.objects.filter(nome_cliente=insere.nome_cliente,cpf=insere.cpf,telefone=insere.telefone)
                clt = user.first().__dict__
                print('Usuário ',str(i+1),' inserido com sucesso')
            except:
                raise Exception('Erro ao inserir usuário ', str(i+1))

            print('Id = ',clt["id_cliente"])
            print('Verificando informações inseridas')
            print("Igualdade em nome_cliente:",testar_igualdade(clt["nome_cliente"],insere.nome_cliente))
            print('Igualdade em cpf:',testar_igualdade(clt["cpf"],insere.cpf))
            print('Igualdade em telefone:',testar_igualdade(clt["telefone"],insere.telefone))

            try:
                user.delete()
                print('Usuário ',str(i+1),' deletado com sucesso')
            except:
                raise Exception('Erro ao deletar usuário ', str(i+1))
            print('-------------------')


        self.stdout.write(self.style.SUCCESS('Teste CT004 concluído com sucesso'))