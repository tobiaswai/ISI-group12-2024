# Generated by Django 5.0.3 on 2024-04-12 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_product_best_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='best_sale',
        ),
    ]