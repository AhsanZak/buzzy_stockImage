# Generated by Django 3.1.3 on 2021-03-11 05:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserSide', '0005_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
