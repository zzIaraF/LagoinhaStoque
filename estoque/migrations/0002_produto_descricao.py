# Generated by Django 4.2.7 on 2023-11-25 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='descricao',
            field=models.TextField(default='Sem descrição'),
        ),
    ]
