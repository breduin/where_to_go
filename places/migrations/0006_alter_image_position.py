# Generated by Django 3.2.8 on 2021-10-31 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_auto_20211031_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='position',
            field=models.SmallIntegerField(default=0, verbose_name='Позиция'),
        ),
    ]
