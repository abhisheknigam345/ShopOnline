# Generated by Django 3.0.2 on 2020-01-21 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Shop_Product', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Quantity', models.PositiveIntegerField()),
                ('Total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('CustomerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ProductId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop_Product.Product')),
            ],
        ),
    ]
