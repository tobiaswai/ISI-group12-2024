# Generated by Django 5.0.3 on 2024-03-10 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_rename_connectivity_technology_product_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='color',
            new_name='connectivity_technology',
        ),
    ]
