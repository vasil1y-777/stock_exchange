# Generated by Django 4.0.4 on 2022-05-17 05:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='trust_points',
            field=models.IntegerField(default=100, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Очки доверия'),
        ),
    ]
