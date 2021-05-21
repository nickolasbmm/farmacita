# FarmacITA

## Requisitos

Primeiramente instale o [python](https://www.python.org/) em uma versão >= 3.8 e o pip.

RECOMENDADO: configurar seu [virtualenv](#Virtualenv)

É necessário instalar todos os módulos do arquivo requirements.txt. Para isso, basta usar o comando:

```shell
python -m pip install -r requirements.txt #linux
py -m pip install -r requirements.txt #windows
```

<sub> Nota: o "python" e o "py" devem se referir ao python de versão >= 3.8. Se você tiver mais de um python instalado vale a pena descobrir qual é o atalho correto para a versão desejada. Podendo ser python3, python3.8, python3m...</sub>

Após instalar os requisitos, rode o script python [test_imports.py](testes/test_imports.py). Ele irá testar se todos os requisitos previstos em requirements.txt estão instalados em sua versão correta.

## Executar o programa

Para iniciar servidor local:

```shell
./runapp  
```

caso o runapp não esteja executável, rodar:

```shell
chmod +x runapp
```

e tentar o ./runapp novamente.

## Virtualenv

### Linux

Para configurar seu virtual env você precisa instalar o python-env primeiro:

```shell
sudo apt-get install python3-env
```

Em seguida você deve ir até a pasta raiz do projeto e criar um environment

```shell
python -m venv ./<nome_do_env>
```

Por último basta ativar o environment (você deve ativá-lo sempre que for rodar python no prrojeto):

```shell
source <nome_do_venv>/bin/activate
```

Quando terminar de usar o projeto desative o environment por boas práticas:

```shell
deactivate
```


##Comandos para instalar django-import-export
```shell
pip install django-import-export
pip install -e git+https://github.com/django-import-export/django-import-export.git#egg=django-import-export
python manage.py collectstatic
```
