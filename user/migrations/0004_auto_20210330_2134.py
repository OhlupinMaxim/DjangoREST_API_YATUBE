# Generated by Django 3.0.5 on 2021-03-30 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210328_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=200, verbose_name='Информация о пользователе'),
        ),
    ]
