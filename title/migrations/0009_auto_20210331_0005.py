# Generated by Django 3.0.5 on 2021-03-30 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0008_auto_20210331_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание произведения'),
        ),
    ]
