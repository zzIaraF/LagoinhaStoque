# Generated by Django 4.2.7 on 2023-11-22 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saidas', '0003_alter_saidas_preco_alter_saidas_precovenda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saidas',
            name='preco',
        ),
        migrations.RemoveField(
            model_name='saidas',
            name='precovenda',
        ),
    ]
