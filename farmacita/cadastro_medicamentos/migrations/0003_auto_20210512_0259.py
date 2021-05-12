# Generated by Django 3.1.3 on 2021-05-12 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro_medicamentos', '0002_principio_ativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='principio_ativo2',
            fields=[
                ('id_principio_ativo2', models.AutoField(primary_key=True, serialize=False)),
                ('nome_principio_ativo2', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='principio_ativo',
        ),
        migrations.CreateModel(
            name='rel_medicamento_principio_ativo2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cadastro_medicamentos.medicamento')),
                ('princ_ativo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cadastro_medicamentos.principio_ativo2')),
            ],
        ),
        migrations.AddField(
            model_name='medicamento',
            name='principio_ativo',
            field=models.ManyToManyField(through='cadastro_medicamentos.rel_medicamento_principio_ativo2', to='cadastro_medicamentos.principio_ativo2'),
        ),
    ]
