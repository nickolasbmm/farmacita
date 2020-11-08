import os
from importlib.metadata import version

this_path = os.path.dirname(os.path.realpath(__file__))
reqs_txt = open(this_path + '/../requirements.txt')
reqs = reqs_txt.read().split('\n')

for req in reqs:
    if '==' in req:

        module, v = req.split('==')

        try:
            module = __import__('_'.join(module.lower().split('-')))

        except:
            print(f'\033[91m{module} não encontrado')

        else:
            if(version(module.__name__) == v):
                print(f'\033[92m{module.__name__} ok')
                
            else:
                print(f'\033[93mVersão de {module} esperada: {v}, versão encontrada: {module.__version__}')
            #else:
             #   print(f'\033[93mNão foi possível verificar a versão do pacote {module.__name__}, por favor verificar manualmente.')