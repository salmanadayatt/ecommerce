# Generated by Django 5.0.6 on 2024-06-03 07:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('shop', '0003_product'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acctnum', models.BigIntegerField()),
                ('accttype', models.CharField(max_length=30)),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_items', models.IntegerField()),
                ('phone', models.BigIntegerField()),
                ('address', models.TextField()),
                ('oredered_date', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.CharField(default='pending', max_length=30)),
                ('delivery_status', models.CharField(default='pending', max_length=30)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
