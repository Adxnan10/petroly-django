# Generated by Django 4.0.6 on 2022-08-20 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0005_alter_cache_age_alter_cache_swr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cache',
            name='data',
            field=models.JSONField(null=True, verbose_name='data'),
        ),
    ]
