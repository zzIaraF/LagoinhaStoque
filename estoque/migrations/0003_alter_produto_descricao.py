# Generated by Django 4.2.5 on 2023-11-26 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0002_produto_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.TextField(default='Sem descrição', null=True),
        ),
    ]
