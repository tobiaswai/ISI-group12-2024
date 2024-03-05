# Generated by Django 5.0.2 on 2024-03-05 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_orderstatus_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderstatuschange',
            name='order',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('cancelled', 'Cancelled'), ('hold', 'Hold')], default='PENDING', max_length=10),
        ),
        migrations.DeleteModel(
            name='OrderStatus',
        ),
        migrations.DeleteModel(
            name='OrderStatusChange',
        ),
    ]