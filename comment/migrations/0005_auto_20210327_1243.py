# Generated by Django 3.0.5 on 2021-03-27 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_comment_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['pub_date']},
        ),
    ]