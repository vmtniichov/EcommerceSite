# Generated by Django 3.2.4 on 2021-11-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]