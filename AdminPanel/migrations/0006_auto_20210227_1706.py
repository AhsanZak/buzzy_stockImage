# Generated by Django 3.1.3 on 2021-02-27 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0005_auto_20210227_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagedetail',
            name='price',
            field=models.BooleanField(default=False, null=True),
        ),
    ]