# Generated by Django 3.2.4 on 2022-01-08 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roommate', '0006_alter_offer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='المستخدم'),
        ),
    ]