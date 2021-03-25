# Generated by Django 3.0.5 on 2021-03-25 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0005_auto_20210325_0048'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0005_auto_20210325_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_title', to='title.Title'),
        ),
    ]
