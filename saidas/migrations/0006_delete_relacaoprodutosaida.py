# Generated by Django 4.2.7 on 2023-11-27 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saidas', '0005_alter_saidas_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RelacaoProdutoSaida',
        ),
    ]