# Generated by Django 5.0.3 on 2024-03-25 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_rename_imgae_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='image'),
        ),
    ]
