# Generated by Django 3.0.5 on 2021-03-27 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_auto_20210325_2147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['pub_date']},
        ),
    ]