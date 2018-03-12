# Generated by Django 2.0.2 on 2018-03-12 18:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0009_despesa_pendente_cadastro_conta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='despesa',
            name='pendente_cadastro_conta',
        ),
        migrations.AlterField(
            model_name='despesa',
            name='mes_termino',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
    ]
