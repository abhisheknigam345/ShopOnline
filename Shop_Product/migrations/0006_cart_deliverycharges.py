# Generated by Django 3.0.2 on 2020-01-25 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_Product', '0005_orderdetail_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='DeliveryCharges',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
