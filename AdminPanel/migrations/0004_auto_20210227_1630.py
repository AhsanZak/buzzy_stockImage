# Generated by Django 3.1.3 on 2021-02-27 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0003_auto_20210227_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
