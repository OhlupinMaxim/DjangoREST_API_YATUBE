# Generated by Django 3.0.5 on 2021-03-24 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0004_auto_20210324_2124'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['pk']},
        ),
    ]
