# Generated by Django 3.0.5 on 2021-03-24 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0005_auto_20210325_0048'),
        ('review', '0002_auto_20210325_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review_title', to='title.Title'),
        ),
    ]
