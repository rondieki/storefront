# Generated by Django 5.0.2 on 2024-03-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0002_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.CharField(max_length=200, null=True),
        ),
    ]