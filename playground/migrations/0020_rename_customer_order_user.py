# Generated by Django 5.0.2 on 2024-03-27 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0019_rename_user_order_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer',
            new_name='user',
        ),
    ]
