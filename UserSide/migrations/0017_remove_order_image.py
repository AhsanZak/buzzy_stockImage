# Generated by Django 3.1.3 on 2021-03-23 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserSide', '0016_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='image',
        ),
    ]
