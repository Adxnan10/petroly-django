# Generated by Django 3.2.10 on 2022-01-10 17:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0008_auto_20220110_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='report',
        ),
        migrations.AddField(
            model_name='community',
            name='reports',
            field=models.ManyToManyField(blank=True, related_name='reported_communities', to=settings.AUTH_USER_MODEL, verbose_name='reports'),
        ),
    ]