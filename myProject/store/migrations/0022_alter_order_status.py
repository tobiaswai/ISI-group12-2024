# Generated by Django 5.0.2 on 2024-03-05 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_remove_orderstatuschange_order_alter_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('cancelled', 'Cancelled'), ('hold', 'Hold')], default='pending', max_length=10),
        ),
    ]
