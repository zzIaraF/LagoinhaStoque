# Generated by Django 4.2.7 on 2023-11-22 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saidas', '0002_alter_saidas_preco_alter_saidas_precovenda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saidas',
            name='preco',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='saidas',
            name='precovenda',
            field=models.FloatField(blank=True),
        ),
    ]
