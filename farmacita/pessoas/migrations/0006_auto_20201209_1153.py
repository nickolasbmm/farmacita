# Generated by Django 3.1.3 on 2020-12-09 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0005_auto_20201209_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='data_de_admissao',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='data_de_demissao',
            field=models.DateField(null=True),
        ),
    ]
