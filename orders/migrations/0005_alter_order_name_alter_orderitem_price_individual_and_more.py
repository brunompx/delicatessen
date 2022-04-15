# Generated by Django 4.0.3 on 2022-04-14 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_ordered_order_complete_alter_order_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(default=238578, max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price_individual',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price_total',
            field=models.FloatField(default=0),
        ),
    ]
