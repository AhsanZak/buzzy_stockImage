# Generated by Django 3.1.3 on 2021-03-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserSide', '0011_auto_20210316_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]