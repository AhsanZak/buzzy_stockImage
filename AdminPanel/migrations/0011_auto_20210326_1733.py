# Generated by Django 3.1.3 on 2021-03-26 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0010_watermark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watermark',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
