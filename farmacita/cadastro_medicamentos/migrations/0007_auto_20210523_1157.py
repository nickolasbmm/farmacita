# Generated by Django 3.1.3 on 2021-05-23 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro_medicamentos', '0006_auto_20210523_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rel_medicamento_principio_ativo2',
            name='medicamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro_medicamentos.medicamento'),
        ),
        migrations.AlterField(
            model_name='rel_medicamento_principio_ativo2',
            name='princ_ativo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro_medicamentos.principio_ativo2'),
        ),
    ]
