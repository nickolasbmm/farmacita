# Generated by Django 3.1.3 on 2020-12-10 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0004_auto_20201210_0134'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordem_de_venda',
            name='valor_total_venda',
            field=models.DecimalField(decimal_places=2, max_digits=40, null=True),
        ),
    ]