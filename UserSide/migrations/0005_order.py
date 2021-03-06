# Generated by Django 3.1.3 on 2021-03-10 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserSide', '0004_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=50, null=True)),
                ('date_ordered', models.DateField(auto_now_add=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('payment_mode', models.CharField(max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
