# Generated by Django 5.0.3 on 2024-05-24 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='shipping_adress',
            new_name='shipping_address',
        ),
    ]