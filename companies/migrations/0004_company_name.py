# Generated by Django 4.0.4 on 2022-05-07 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_alter_company_managers_remove_company_shareholders_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='name',
            field=models.CharField(default=None, max_length=255, unique=True, verbose_name='Название компании'),
            preserve_default=False,
        ),
    ]
