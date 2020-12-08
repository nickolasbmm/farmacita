# Generated by Django 3.1.3 on 2020-12-08 21:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nome_cliente', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=14)),
                ('telefone', models.CharField(max_length=15)),
                ('data_nascimento', models.DateField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='fornecedor',
            fields=[
                ('id_fornecedor', models.AutoField(primary_key=True, serialize=False)),
                ('nome_fornecedor', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=18)),
                ('telefone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_funcionario', models.CharField(max_length=300)),
                ('cpf', models.CharField(max_length=14)),
                ('telefone', models.CharField(max_length=15)),
                ('cargo', models.CharField(max_length=100)),
                ('data_de_admissao', models.DateTimeField()),
                ('data_de_demissao', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
