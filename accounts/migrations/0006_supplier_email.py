# Generated by Django 3.0.2 on 2020-01-27 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200127_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='Email',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]