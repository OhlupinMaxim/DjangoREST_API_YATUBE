# Generated by Django 3.0.5 on 2021-03-24 23:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review_author', to=settings.AUTH_USER_MODEL),
        ),
    ]
