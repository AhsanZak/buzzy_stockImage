# Generated by Django 3.1.3 on 2021-03-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserSide', '0022_wallettransactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettransactions',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]