# Generated by Django 3.0.5 on 2021-03-30 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0007_auto_20210331_0001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('slug',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('slug',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
    ]