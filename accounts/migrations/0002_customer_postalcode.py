# Generated by Django 3.0.2 on 2020-01-19 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='PostalCode',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]