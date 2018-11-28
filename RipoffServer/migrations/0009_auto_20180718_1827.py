# Generated by Django 2.0.5 on 2018-07-19 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RipoffServer', '0008_auto_20180718_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rdaplan',
            name='base_cost',
            field=models.IntegerField(verbose_name='Plan Base Cost'),
        ),
        migrations.AlterField(
            model_name='rdaplan',
            name='dollars',
            field=models.IntegerField(verbose_name='RDA Dollars'),
        ),
        migrations.AlterField(
            model_name='rdaplan',
            name='plan',
            field=models.IntegerField(verbose_name='Plan Number'),
        ),
    ]
