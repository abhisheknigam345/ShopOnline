# Generated by Django 3.0.2 on 2020-01-27 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customer_locationid'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='Password',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='SupplierUserName',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
