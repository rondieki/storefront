# Generated by Django 5.0.2 on 2024-03-25 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0013_cart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
