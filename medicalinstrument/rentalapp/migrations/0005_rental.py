# Generated by Django 5.0.6 on 2024-06-26 06:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0004_product_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('return_date', models.DateField()),
                ('total_days', models.CharField(max_length=150)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentalapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentalapp.register')),
            ],
        ),
    ]
