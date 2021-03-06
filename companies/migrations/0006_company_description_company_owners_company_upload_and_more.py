# Generated by Django 4.0.4 on 2022-05-15 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0005_delete_shares'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='description',
            field=tinymce.models.HTMLField(help_text='Опишите компанию', max_length=1024, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='company',
            name='owners',
            field=models.ManyToManyField(related_name='companies', to=settings.AUTH_USER_MODEL, verbose_name='Владельцы'),
        ),
        migrations.AddField(
            model_name='company',
            name='upload',
            field=models.ImageField(blank=True, upload_to='uploads/', verbose_name='Логотип компании'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.ImageField(null=True, upload_to='uploads/')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='gallery',
            field=models.ManyToManyField(blank=True, related_name='companies', to='companies.photo', verbose_name='Фотографии'),
        ),
    ]
