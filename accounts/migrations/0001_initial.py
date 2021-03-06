# Generated by Django 3.0.2 on 2020-01-11 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CompanyName', models.CharField(max_length=100)),
                ('PhoneNumber', models.CharField(max_length=100)),
                ('Mobile', models.CharField(max_length=100)),
                ('Country', models.CharField(max_length=50)),
                ('Address', models.CharField(max_length=120)),
                ('CustomerId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
