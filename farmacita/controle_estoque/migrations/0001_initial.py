# Generated by Django 3.1.3 on 2020-12-08 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pessoas', '0001_initial'),
        ('cadastro_medicamentos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='lote_medicamento',
            fields=[
                ('id_lote_medicamento', models.AutoField(primary_key=True, serialize=False)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=40)),
                ('quantidade_de_caixas', models.CharField(max_length=100)),
                ('quantidade_por_caixa', models.CharField(max_length=100)),
                ('dosagem', models.CharField(max_length=100)),
                ('data_de_validade', models.DateTimeField()),
                ('industria_farmaceutica', models.CharField(max_length=100)),
                ('excluido', models.BooleanField(default=False)),
                ('id_fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoas.fornecedor')),
                ('id_medicamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cadastro_medicamentos.medicamento')),
            ],
        ),
    ]
