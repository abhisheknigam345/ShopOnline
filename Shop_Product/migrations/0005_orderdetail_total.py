# Generated by Django 3.0.2 on 2020-01-24 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Product', '0004_order_orderdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='Total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
