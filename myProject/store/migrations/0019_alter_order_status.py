# Generated by Django 5.0.1 on 2024-03-04 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_product_size_product_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]