# Generated by Django 3.1.3 on 2020-12-09 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_estoque', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote_medicamento',
            name='data_de_validade',
            field=models.DateField(),
        ),
    ]