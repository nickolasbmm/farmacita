# Generated by Django 3.1.3 on 2021-05-12 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0005_ordem_de_venda_valor_total_venda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordem_de_venda',
            name='data_de_venda',
            field=models.DateField(auto_now=True),
        ),
    ]