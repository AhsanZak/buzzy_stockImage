# Generated by Django 3.1.3 on 2021-02-28 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0007_remove_imagedetail_type'),
        ('UserSide', '0002_auto_20210224_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Downloads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateField(auto_now_add=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('payment_mode', models.CharField(max_length=50, null=True)),
                ('payment_status', models.CharField(max_length=50, null=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminPanel.imagedetail')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
