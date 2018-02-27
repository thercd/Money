# Generated by Django 2.0.2 on 2018-02-27 17:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0004_auto_20180227_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]