# Generated by Django 2.0.2 on 2018-03-02 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0004_auto_20180302_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='referente',
            field=models.DateField(),
        ),
    ]
